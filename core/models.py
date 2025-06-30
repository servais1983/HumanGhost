from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Table pour les configurations globales et les secrets
class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(200), nullable=True)

# Nouveaux modèles pour les ressources de campagne
class EmailTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False) # Contenu HTML

class PageTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    html_content = db.Column(db.Text, nullable=False)

class TargetGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    targets = db.Column(db.Text, nullable=False) # Liste d'emails, un par ligne

# La table Campaign est maintenant liée aux nouvelles ressources
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    email_template_id = db.Column(db.Integer, db.ForeignKey('email_template.id'))
    page_template_id = db.Column(db.Integer, db.ForeignKey('page_template.id'))
    target_group_id = db.Column(db.Integer, db.ForeignKey('target_group.id'))
    
    email_template = db.relationship('EmailTemplate')
    page_template = db.relationship('PageTemplate')
    target_group = db.relationship('TargetGroup')
    
    events = db.relationship('Event', backref='campaign', lazy=True, cascade="all, delete-orphan")

class Event(db.Model):
    # Le modèle Event ne change pas
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    event_type = db.Column(db.String(50))
    details = db.Column(db.String(255))
