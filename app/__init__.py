from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message

from config import Develop

app = Flask(__name__)
app.config.from_object(Develop)


db = SQLAlchemy(app)

from app import models

migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)
with app.app_context():
    msg = Message("Subject", recipients=['ebedak2003@yandex.ru'])
msg.body = 'Body message'
mail.send(msg)


def get_session() -> db.Session:
    return db.session
