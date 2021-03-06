from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_restful import Api
from flask_script import Manager

from config import Production

app = Flask(__name__)
app.config.from_object(Production)

db = SQLAlchemy(app)


def get_session() -> db.Session:
    return db.session


def send_mail(msg):
    with app.app_context():
        mail.send(msg)


login_manager = LoginManager(app)
mail = Mail(app)
api = Api(app)

from app import models, user_api, post_api
from app.blueprints.user import blueprint_user
from app.blueprints.post import blueprint_post
from app.blueprints.main import main_blueprint

api.add_resource(user_api.UserResource, '/user-api', '/user-api/<int:user_id>')
api.add_resource(post_api.PostResource, '/post-api', '/post-api/<int:post_id>')
app.register_blueprint(blueprint_user)
app.register_blueprint(blueprint_post)
app.register_blueprint(main_blueprint)

migrate = Migrate()
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
manager = Manager(app)
