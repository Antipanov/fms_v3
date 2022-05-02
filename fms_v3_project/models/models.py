from ..extensions import db
from datetime import datetime, date

"""Модель для соревнований"""
class CompetitionsDB(db.Model):
    competition_id = db.Column(db.Integer, primary_key=True)
    competition_name = db.Column(db.String)
    competition_date_start = db.Column(db.Date, default=datetime.utcnow)
    competition_date_finish = db.Column(db.Date, default=datetime.utcnow)
    competition_city = db.Column(db.String)
    # competition_fights = db.relationship('FightsDB', backref='competition', lazy='dynamic')
    # registrations = db.relationship('RegistrationDB', backref='competition')
