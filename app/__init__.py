from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_restful import Api
from flask_script import Manager

from config import Develop, Testing

app = Flask(__name__)
app.config.from_object(Develop)

db = SQLAlchemy(app)


def get_session() -> db.Session:
    return db.session


from app import models, user_api

api = Api(app)
api.add_resource(user_api.UserResource, '/user-api', '/user-api/<int:user_id>')

migrate = Migrate()
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
login_manager = LoginManager(app)
mail = Mail(app)
manager = Manager(app)
