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


login_manager = LoginManager(app)
mail = Mail(app)
api = Api(app)

from app import models, user_api
from app.blueprints.user import blueprint_user
from app.blueprints.post import blueprint_post

api.add_resource(user_api.UserResource, '/user-api', '/user-api/<int:user_id>')
app.register_blueprint(blueprint_user)
app.register_blueprint(blueprint_post)

migrate = Migrate()
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
manager = Manager(app)
