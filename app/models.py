from app import db

from flask_sqlalchemy import BaseQuery
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    importance = db.Column(db.Integer)
    create_date = db.Column(db.Date, default=datetime.now())

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_query() -> BaseQuery:
        return User.query
