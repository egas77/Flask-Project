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
    nickname = db.Column(db.String)
    importance = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now())
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_date = db.Column(db.DateTime)
    registration_date = db.Column(db.Date, default=datetime.date.today())
    subscription = db.Column(db.Boolean, default=False)
    image_file = db.Column(db.String)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {} {}>'.format(self.login, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_query() -> BaseQuery:
        return User.query


class Post(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    publication_date = db.Column(db.DateTime, default=datetime.datetime.now())
    publication_date_string = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Post {} {}'.format(self.title, self.id)

    @staticmethod
    def get_query() -> BaseQuery:
        return Post.query
