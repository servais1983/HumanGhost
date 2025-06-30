from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Crée une instance de SQLAlchemy qui sera liée à notre application Flask
db = SQLAlchemy()

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Event', backref='campaign', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    event_type = db.Column(db.String(50)) # Ex: 'Visit', 'Credential Submission'
    details = db.Column(db.String(255))
