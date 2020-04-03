from app import db

from flask_sqlalchemy import BaseQuery
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash
import datetime


class User(db.Model, UserMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    username = db.Column(db.String)
    importance = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now())
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.login)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_query() -> BaseQuery:
        return User.query
