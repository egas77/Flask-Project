from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    importance = db.Column(db.Integer)
    create_date = db.Column(db.Date, default=datetime.now())

    def __repr__(self):
        return '<User {}>'.format(self.username)
