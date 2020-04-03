from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_restful import Api
from flask_socketio import SocketIO

from config import Develop, Testing

app = Flask(__name__)
app.config.from_object(Develop)

db = SQLAlchemy(app)


def get_session() -> db.Session:
    return db.session


from app import models, user_api

api = Api(app)
api.add_resource(user_api.UserResource, '/user-api')

migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)
socket = SocketIO(app)
