from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_socketio import SocketIO
from weasyprint import HTML
import threading
import os
from datetime import datetime

# Importation de la nouvelle structure de la base de données
from .models import db, Setting, EmailTemplate, PageTemplate, TargetGroup, Campaign, Event
# Importation des modules de logique métier
from . import send, llm_generator, qr_generator

socketio = SocketIO()

def create_app():
    """
    Fonction 'Factory' pour créer l'application Flask principale.
    C'est ici que toute la logique de l'interface web est définie.
    """
    app = Flask(__name__, template_folder=os.path.abspath('templates'))
    app.config['SECRET_KEY'] = 'humanghost-c2-super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///humanghost.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all() # Crée la base de données et les tables si elles n'existent pas

    # --- ROUTES PRINCIPALES DE GESTION ---
    @app.route("/")
    def index():
        return redirect(url_for('dashboard'))

    @app.route("/dashboard")
    def dashboard():
        campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
        return render_template("dashboard.html", campaigns=campaigns, page='dashboard')

    @app.route("/settings", methods=['GET', 'POST'])
    def settings():
        if request.method == 'POST':
            # Sauvegarde de chaque paramètre dans la base de données
            for key, value in request.form.items():
                setting = Setting.query.filter_by(key=key).first()
                if setting:
                    setting.value = value
                else:
                    db.session.add(Setting(key=key, value=value))
            db.session.commit()
            flash("Paramètres sauvegardés avec succès !", 'success')
            return redirect(url_for('settings'))
        
        # Charge les paramètres existants pour les afficher dans le formulaire
        settings = {s.key: s.value for s in Setting.query.all()}
        return render_template("settings.html", settings=settings, page='settings')

    @app.route("/campaign-launcher", methods=['GET', 'POST'])
    def campaign_launcher():
        if request.method == 'POST':
            # Logique pour lancer une nouvelle campagne
            new_campaign = Campaign(
                name=request.form['name'],
                email_template_id=request.form['email_template_id'],
                page_template_id=request.form['page_template_id'],
                target_group_id=request.form['target_group_id']
            )
            db.session.add(new_campaign)
            db.session.commit()
            
            # --- DÉCLENCHEMENT DE LA LOGIQUE D'ENVOI ---
            # Il faudrait ici une file d'attente (comme Celery), mais pour l'instant, on lance directement
            execute_campaign(new_campaign.id)
            
            flash(f"Campagne '{new_campaign.name}' lancée !", 'success')
            return redirect(url_for('dashboard'))

        # Charge les ressources nécessaires pour les menus déroulants
        email_templates = EmailTemplate.query.all()
        page_templates = PageTemplate.query.all()
        target_groups = TargetGroup.query.all()
        return render_template("campaign_launcher.html", 
                               email_templates=email_templates,
                               page_templates=page_templates,
                               target_groups=target_groups,
                               page='launcher')

    # --- ROUTES DU SERVEUR DE PHISHING (le "payload") ---
    # Ces routes sont dynamiques et leur logique dépendra de la campagne active
    # (Cette partie nécessite une refonte plus complexe pour gérer plusieurs campagnes simultanément)
    # Pour l'instant, nous la laissons conceptuelle.

    socketio.init_app(app)
    return app

def run_server(host, port):
    """
    Point d'entrée pour démarrer le serveur.
    """
    app = create_app()
    print(f"[*] Plateforme de gestion accessible sur http://{host}:{port}")
    socketio.run(app, host=host, port=port, allow_unsafe_werkzeug=True)

def execute_campaign(campaign_id):
    """
    Fonction qui exécute la logique d'une campagne (envoi d'emails).
    Elle devrait tourner en arrière-plan.
    """
    print(f"[*] Exécution de la logique pour la campagne ID: {campaign_id}")
    app = create_app() # Crée un contexte d'application pour accéder à la DB
    with app.app_context():
        campaign = Campaign.query.get(campaign_id)
        settings = {s.key: s.value for s in Setting.query.all()}

        # Vérifie que la configuration SMTP est présente
        if not all(k in settings for k in ['smtp_host', 'smtp_port', 'smtp_user', 'smtp_pass']):
            print("[!] ERREUR: Configuration SMTP incomplète dans les paramètres.")
            return

        smtp_config = {
            'host': settings['smtp_host'],
            'port': int(settings['smtp_port']),
            'username': settings['smtp_user'],
            'password': settings['smtp_pass'],
            'sender_email': settings['smtp_sender']
        }

        targets = campaign.target_group.targets.strip().split('\n')
        print(f"[*] Envoi de la campagne à {len(targets)} cible(s)...")

        for target_email in targets:
            # Ici, on pourrait utiliser le LLM si configuré...
            # Pour l'instant, on utilise le template directement.
            send.send_email(
                smtp_config=smtp_config,
                target_email=target_email.strip(),
                subject=campaign.email_template.subject,
                body=campaign.email_template.body # Le body contient déjà le HTML complet
            )
