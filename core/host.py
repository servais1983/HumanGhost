from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from flask_socketio import SocketIO
from weasyprint import HTML
import threading
import os
from datetime import datetime

# Importation de la structure complète de la base de données
from .models import db, Setting, EmailTemplate, PageTemplate, TargetGroup, Campaign, Event
# Importation des modules de logique métier
from . import send, llm_generator, qr_generator

# Instance globale de SocketIO
socketio = SocketIO()

def create_app():
    """
    Fonction 'Factory' pour créer et configurer l'application Flask principale.
    C'est ici que toute la logique de l'interface web est définie.
    """
    app = Flask(__name__, template_folder=os.path.abspath('templates'))
    app.config['SECRET_KEY'] = 'humanghost-c2-super-secret-key-make-it-long-and-random'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///humanghost.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisation de la base de données avec l'application
    db.init_app(app)

    with app.app_context():
        # Crée la base de données et toutes les tables si elles n'existent pas déjà
        db.create_all()

    # --- ROUTES PRINCIPALES DE L'INTERFACE DE GESTION ---

    @app.route("/")
    def index():
        """Redirige vers le tableau de bord principal."""
        return redirect(url_for('dashboard'))

    @app.route("/dashboard")
    def dashboard():
        """Affiche le tableau de bord avec la liste des campagnes."""
        campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
        return render_template("dashboard.html", campaigns=campaigns, page='dashboard')

    @app.route("/settings", methods=['GET', 'POST'])
    def settings():
        """Gère la configuration globale (SMTP, API keys)."""
        if request.method == 'POST':
            for key, value in request.form.items():
                setting = Setting.query.filter_by(key=key).first()
                if setting:
                    setting.value = value
                else:
                    db.session.add(Setting(key=key, value=value))
            db.session.commit()
            flash("Paramètres sauvegardés avec succès !", 'success')
            return redirect(url_for('settings'))
        
        settings = {s.key: s.value for s in Setting.query.all()}
        return render_template("settings.html", settings=settings, page='settings')

    @app.route("/resources")
    def resources():
        """Affiche le hub de gestion des ressources."""
        return render_template("manage_resources.html", page='resources')

    # --- GESTION DES RESSOURCES (CRUD) ---

    # Templates d'E-mail
    @app.route("/resources/email-templates")
    def manage_email_templates():
        templates = EmailTemplate.query.all()
        return render_template("manage_list.html", items=templates, title="Templates d'E-mail", create_url=url_for('create_email_template'))

    @app.route("/resources/email-templates/new", methods=['GET', 'POST'])
    def create_email_template():
        if request.method == 'POST':
            new_template = EmailTemplate(name=request.form['name'], subject=request.form['subject'], body=request.form['body'])
            db.session.add(new_template)
            db.session.commit()
            return redirect(url_for('manage_email_templates'))
        fields = [{'name': 'name', 'label': 'Nom du Template'}, {'name': 'subject', 'label': 'Sujet'}, {'name': 'body', 'label': 'Corps HTML', 'type': 'textarea'}]
        return render_template("crud_form.html", title="Créer un Template d'E-mail", fields=fields, action="Créer", value={})

    # Templates de Page
    @app.route("/resources/page-templates")
    def manage_page_templates():
        templates = PageTemplate.query.all()
        return render_template("manage_list.html", items=templates, title="Templates de Page", create_url=url_for('create_page_template'))

    @app.route("/resources/page-templates/new", methods=['GET', 'POST'])
    def create_page_template():
        if request.method == 'POST':
            new_template = PageTemplate(name=request.form['name'], html_content=request.form['html_content'])
            db.session.add(new_template)
            db.session.commit()
            return redirect(url_for('manage_page_templates'))
        fields = [{'name': 'name', 'label': 'Nom du Template'}, {'name': 'html_content', 'label': 'Contenu HTML complet', 'type': 'textarea'}]
        return render_template("crud_form.html", title="Créer un Template de Page", fields=fields, action="Créer", value={})

    # Groupes de Cibles
    @app.route("/resources/target-groups")
    def manage_target_groups():
        groups = TargetGroup.query.all()
        return render_template("manage_list.html", items=groups, title="Groupes de Cibles", create_url=url_for('create_target_group'))

    @app.route("/resources/target-groups/new", methods=['GET', 'POST'])
    def create_target_group():
        if request.method == 'POST':
            new_group = TargetGroup(name=request.form['name'], targets=request.form['targets'])
            db.session.add(new_group)
            db.session.commit()
            return redirect(url_for('manage_target_groups'))
        fields = [{'name': 'name', 'label': 'Nom du Groupe'}, {'name': 'targets', 'label': 'Emails des Cibles (un par ligne)', 'type': 'textarea'}]
        return render_template("crud_form.html", title="Créer un Groupe de Cibles", fields=fields, action="Créer", value={})

    # --- LANCEUR DE CAMPAGNE ET LOGIQUE MÉTIER ---

    @app.route("/campaign-launcher", methods=['GET', 'POST'])
    def campaign_launcher():
        """Affiche le formulaire pour lancer une nouvelle campagne."""
        if request.method == 'POST':
            new_campaign = Campaign(
                name=request.form['name'],
                email_template_id=request.form['email_template_id'],
                page_template_id=request.form['page_template_id'],
                target_group_id=request.form['target_group_id']
            )
            db.session.add(new_campaign)
            db.session.commit()
            
            # Déclenche l'envoi dans un thread pour ne pas bloquer l'interface
            threading.Thread(target=execute_campaign_in_context, args=(new_campaign.id,)).start()
            
            flash(f"Campagne '{new_campaign.name}' lancée avec succès !", 'success')
            return redirect(url_for('dashboard'))

        email_templates = EmailTemplate.query.all()
        page_templates = PageTemplate.query.all()
        target_groups = TargetGroup.query.all()
        return render_template("campaign_launcher.html", 
                               email_templates=email_templates,
                               page_templates=page_templates,
                               target_groups=target_groups,
                               page='launcher')

    # --- API et Rapports ---

    @app.route("/api/campaign/<int:campaign_id>/events")
    def get_events(campaign_id):
        """API pour que le tableau de bord récupère les événements d'une campagne."""
        events = Event.query.filter_by(campaign_id=campaign_id).order_by(Event.timestamp.desc()).all()
        return jsonify([event_to_dict(e) for e in events])

    @app.route("/report/campaign/<int:campaign_id>")
    def download_report(campaign_id):
        """Génère et sert un rapport PDF pour une campagne donnée."""
        campaign = Campaign.query.get_or_404(campaign_id)
        events = Event.query.filter_by(campaign_id=campaign_id).order_by(Event.timestamp.asc()).all()
        
        visits = sum(1 for e in events if e.event_type == 'Visit')
        credentials_captured = sum(1 for e in events if 'Credential' in e.event_type)
        success_rate = (credentials_captured / visits) if visits > 0 else 0
        stats = {'total_events': len(events), 'visits': visits, 'credentials_captured': credentials_captured, 'success_rate': success_rate}

        html_string = render_template("report_template.html", campaign=campaign, events=events, stats=stats)
        pdf = HTML(string=html_string).write_pdf()
        
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=rapport_campagne_{campaign_id}.pdf'
        return response

    # Initialise SocketIO avec l'application
    socketio.init_app(app)
    return app

def run_server(host, port):
    """Point d'entrée unique pour démarrer le serveur, appelé par la CLI."""
    app = create_app()
    socketio.run(app, host=host, port=port, allow_unsafe_werkzeug=True)

def execute_campaign_in_context(campaign_id):
    """Fonction qui crée un contexte d'application pour exécuter la logique d'une campagne."""
    app = create_app()
    with app.app_context():
        execute_campaign(campaign_id)

def execute_campaign(campaign_id):
    """Exécute la logique d'envoi d'une campagne."""
    print(f"[*] Début de l'exécution de la campagne ID: {campaign_id}")
    campaign = Campaign.query.get(campaign_id)
    settings = {s.key: s.value for s in Setting.query.all()}
    
    required_settings = ['smtp_host', 'smtp_port', 'smtp_user', 'smtp_pass', 'smtp_sender']
    if not all(k in settings and settings[k] for k in required_settings):
        print(f"[!] ERREUR [Campagne {campaign_id}]: Configuration SMTP incomplète dans les Paramètres.")
        return

    smtp_config = {'host': settings['smtp_host'], 'port': int(settings['smtp_port']), 'username': settings['smtp_user'], 'password': settings['smtp_pass'], 'sender_email': settings['smtp_sender']}
    targets = campaign.target_group.targets.strip().split('\n')
    print(f"[*] [Campagne {campaign_id}] Envoi à {len(targets)} cible(s)...")

    for target_email in targets:
        if not target_email.strip(): continue
        send.send_email(smtp_config=smtp_config, target_email=target_email.strip(), subject=campaign.email_template.subject, body=campaign.email_template.body)

def event_to_dict(event):
    """Utilitaire pour convertir un objet Event en dictionnaire pour l'API et SocketIO."""
    return {
        'campaign_id': event.campaign_id,
        'timestamp': event.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'credential' if 'Credential' in event.event_type else 'event',
        'event': event.event_type,
        'details': event.details or f"IP: {event.ip_address}"
    }

# NOTE : La logique pour les routes de phishing actives (`/` et `/login`) devrait être rendue
# plus dynamique pour gérer plusieurs campagnes simultanément, par exemple en utilisant des URL
# uniques par campagne (ex: /track/<campaign_uuid>). Pour la clarté du code final, cette
# complexité supplémentaire a été omise.
