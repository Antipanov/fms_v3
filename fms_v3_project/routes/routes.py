from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from ..extensions import db
from ..models.models import CompetitionsDB, RegistrationDB, FightersDB
from ..forms import CompetitionForm
from sqlalchemy import desc, asc

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/')
def home_view():
    return "homepage"


# Список соревнований
competitions = Blueprint('competitions', __name__, template_folder='templates')


@competitions.route('/competitions')
def competitions_view():
    competitions_data = CompetitionsDB.query.filter_by(delete_status=False).order_by(asc(CompetitionsDB.competition_date_start)).all()
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
            return render_template('competition.html', form=form, competition_data=created_competition_data)

        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template('newcompetition.html')


# Карточка соревнования
# competition view
@competitions.route('/competitions/<int:competition_id>')
def competition_view(competition_id):
    competition_data = CompetitionsDB.query.get(competition_id)
    competitions_data = db.session.query(CompetitionsDB.competition_id).filter_by(delete_status = False).all()
    competition_id_list = [value for value, in competitions_data]
    if competition_id in competition_id_list:
        return render_template('competition.html', competition_data=competition_data)
    else:
        return redirect(url_for('competitions.competitions_view'))


# генерация отображения содержимого модала удаления соревнования
@competitions.route('/ajaxfile_delete_comp', methods=["POST", "GET"])
def ajaxfile_delete_competition_func():
    if request.method == 'POST':
        competition_id = request.form['competition_id']
        competition_data = CompetitionsDB.query.filter_by(competition_id=competition_id, delete_status=False).all()
        comp_regs_data = RegistrationDB.query.filter_by(competition_id=competition_id).all()
        number_of_registrations = len(comp_regs_data)
        if number_of_registrations==0:
            return jsonify({'htmlresponse': render_template('response_compet_delete.html', competition_data=competition_data)})
        else:
            return jsonify({'htmlresponse': render_template('response_compet_no_delete.html', competition_data=competition_data)})
# генерация отображения формы редактирования соревнования
@competitions.route('/ajaxfile', methods=["POST", "GET"])
def ajaxfile():
    if request.method == 'POST':
        competition_id = request.form['competition_id']
        form = CompetitionForm()
        competition_data = CompetitionsDB.query.filter_by(competition_id=competition_id).all()
        return jsonify({'htmlresponse': render_template('response.html', competition_data=competition_data, form=form)})


# competition view
@competitions.route('/competitions/edit/<int:competition_id>', methods=["POST", "GET"])
def competition_edit_view(competition_id):
    competition_data = CompetitionsDB.query.get(competition_id)
    competitions_data = CompetitionsDB.query.order_by(asc(CompetitionsDB.competition_date_start)).all()
    form = CompetitionForm()
    if form.validate_on_submit():
        flash('Изменения сохранены')
        competition_data.competition_name = form.competition_name_form.data
        competition_data.competition_date_start = form.competition_date_start.data
        competition_data.competition_date_finish = form.competition_date_finish.data
        competition_data.competition_city = form.competition_city.data
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

        return redirect(url_for('competitions.competitions_view'))
    return render_template('competitions.html', competitions_data=competitions_data)

# удаление соревнования
@competitions.route('/competitions/delete/<int:competition_id>')
def competition_delete_view(competition_id):
    competition_data = CompetitionsDB.query.get(competition_id)
    print(type(competition_data))
    competition_data.delete_status = True
    try:
        db.session.commit()
        flash('Изменения сохранены')
    except Exception as e:
        print("ошибка при сохранении изменений в БД: ", e)
        db.session.rollback()
    return redirect(url_for('competitions.competitions_view'))

import csv
from datetime import date
@home.route('/fill_fighters')
def fill_fighters():
    with open('fighters.csv', encoding='utf8') as csvfile:
        fighters_csv_list = csv.reader(csvfile)
        for row in fighters_csv_list:
            new_fighter = FightersDB(active_status=True, first_name = row[0], last_name=row[1], fighter_image_id = row[2], birthday=date(int(row[3]),int(row[4]),int(row[5])))
            db.session.add(new_fighter)
            try:
                db.session.commit()
            except Exception as e:
                print("Не получилось импортировать бойцов. Ошибка: ", e)
                db.session.rollback()
    return "Бойцы импортированы в базу"
