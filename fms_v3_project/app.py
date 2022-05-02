from flask import Flask
from .extensions import db, migrate
from .routes.routes import home, competitions


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fights.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db)
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.register_blueprint(home)
app.register_blueprint(competitions)
# db.create_all()


if __name__ == "__main__":
    app.run()