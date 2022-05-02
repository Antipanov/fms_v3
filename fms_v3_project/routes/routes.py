from flask import Blueprint, render_template
from ..models.models import CompetitionsDB

home = Blueprint('home', __name__, template_folder='templates')
@home.route('/')
def home_view():
    return "homepage"


# Competitions list
competitions = Blueprint('competitions', __name__, template_folder='templates')
@competitions.route('/competitions')
def competitions_view():
    competitions_data = CompetitionsDB.query.all()
    return render_template('competitions.html', competitions_data=competitions_data)
