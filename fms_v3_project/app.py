from flask import Flask
from .extensions import db, migrate
from .routes.routes import home, competitions, fighters





app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fights.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.register_blueprint(home)
app.register_blueprint(competitions)
app.register_blueprint(fighters)
# competitions.competition_create_new = 'competitions.competition_create_new'

if __name__ == "__main__":
    app.run()
