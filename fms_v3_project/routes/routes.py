from flask import Blueprint, render_template, flash
from ..extensions import db
from ..models.models import CompetitionsDB
from ..forms import CompetitionForm
from sqlalchemy import desc

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/')
def home_view():
    return "homepage"


# Список соревнований
competitions = Blueprint('competitions', __name__, template_folder='templates')


@competitions.route('/competitions')
def competitions_view():
    competitions_data = CompetitionsDB.query.all()
    return render_template('competitions.html', competitions_data=competitions_data)


# Форма создания нового соревнования
@competitions.route('/competitions/new', methods=["POST", "GET"])
def competition_create_new():
    form = CompetitionForm()
    return render_template('newcompetition.html', form=form)

# Действие по кнопке создания нового соревнования
@competitions.route('/competitions/created_new', methods=["POST", "GET"])
def form_action_competition_create_new():
    form = CompetitionForm()
    if form.validate_on_submit():
        new_competition = CompetitionsDB(competition_name=form.competition_name_form.data,
                                         competition_date_start=form.competition_date_start.data,
                                         competition_date_finish=form.competition_date_finish.data,
                                         competition_city=form.competition_city.data,
                                         )
        db.session.add(new_competition)
        try:
            db.session.commit()
            created_competition_data = CompetitionsDB.query.order_by(desc(CompetitionsDB.competition_id)).first()
            flash('Изменения сохранены')
            return render_template('competition.html', form=form, competition_data=created_competition_data, flash=flash)

        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template('newcompetition.html')

