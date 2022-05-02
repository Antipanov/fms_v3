from flask import Flask
from extensions import db, migrate
from routes.routes import home


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fights.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db.init_app(app)
migrate.init_app(app, db)
app.register_blueprint(home)



if __name__ == "__main__":
    app.run()