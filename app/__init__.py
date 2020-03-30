from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Develop, Production

app = Flask(__name__)
app.config.from_object(Develop)

db = SQLAlchemy(app)

from app import models

migrate = Migrate(app, db)
