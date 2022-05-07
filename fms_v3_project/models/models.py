from ..extensions import db
from datetime import datetime, date

"""Модель для соревнований"""
class CompetitionsDB(db.Model):
    competition_id = db.Column(db.Integer, primary_key=True)
    competition_name = db.Column(db.String)
    competition_date_start = db.Column(db.Date, default=datetime.utcnow)
    competition_date_finish = db.Column(db.Date, default=datetime.utcnow)
    competition_city = db.Column(db.String)
    delete_status = db.Column(db.Boolean, default=False)
    registrations = db.relationship('RegistrationDB', backref='competition')
    # competition_fights = db.relationship('FightsDB', backref='competition', lazy='dynamic')
    # registrations = db.relationship('RegistrationDB', backref='competition')
"""Модель для регистрации"""
class RegistrationDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitionsDB.competition_id'))
    # fighter_id = db.Column(db.Integer, db.ForeignKey('fightersDB.fighter_id'))
    fighter_registration_weight = db.Column(db.Integer)
    fighter_registration_age = db.Column(db.Integer)
    # weight_cat_id = db.Column(db.Integer, db.ForeignKey('weightcategoriesDB.weight_cat_id'))
    # age_cat_id = db.Column(db.Integer, db.ForeignKey('agecategoriesDB.id'))