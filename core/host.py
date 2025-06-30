# ... (importations existantes) ...
from flask import make_response
from weasyprint import HTML, CSS
from .models import db, Campaign, Event

# ... (la fonction create_app et les autres routes restent les mêmes) ...

def create_app(config):
    # ... (le début de la fonction create_app reste identique) ...
    # ... (les routes '/', '/login', '/dashboard', '/api/campaign/<id>/events' ne changent pas) ...

    @app.route("/report/campaign/<int:campaign_id>")
    def download_report(campaign_id):
        """
        Génère et sert un rapport PDF pour une campagne donnée.
        """
        campaign = Campaign.query.get_or_404(campaign_id)
        events = Event.query.filter_by(campaign_id=campaign_id).order_by(Event.timestamp.asc()).all()
        
        # Calcul des statistiques
        visits = sum(1 for e in events if e.event_type == 'Visit')
        credentials_captured = sum(1 for e in events if e.event_type == 'Credential Submission')
        success_rate = (credentials_captured / visits) if visits > 0 else 0
        
        stats = {
            'total_events': len(events),
            'visits': visits,
            'credentials_captured': credentials_captured,
            'success_rate': success_rate
        }

        # Rendu du template HTML
        html_string = render_template("report_template.html", campaign=campaign, events=events, stats=stats)
        
        # Génération du PDF
        pdf = HTML(string=html_string).write_pdf()
        
        # Création de la réponse HTTP
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=rapport_campagne_{campaign_id}.pdf'
        
        return response

    socketio.init_app(app)
    return app

# ... (les autres fonctions du fichier ne changent pas) ...
