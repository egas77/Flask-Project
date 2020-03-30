class Config(object):
    SECRET_KEY = 'LMTk06lLwpD4HlZl'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'main.py'


class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
