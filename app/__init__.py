from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Develop

app = Flask(__name__)
app.config.from_object(Develop)

db = SQLAlchemy(app)

from app import models

migrate = Migrate(app, db)
login_manager = LoginManager(app)


def get_session() -> db.Session:
    return db.session
