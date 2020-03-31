class Config(object):
    SECRET_KEY = 'LMTk06lLwpD4HlZl'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'main.py'
    RECAPTCHA_PUBLIC_KEY = '6LfcguUUAAAAAMWvFiu8rpazGR61ZxuIDbtkaG65'
    RECAPTCHA_PRIVATE_KEY = '6LfcguUUAAAAAEWzpN78kxcUj31kU8FAuQn2UG8S'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'blogflask89@gmail.com'
    MAIL_DEFAULT_SENDER = 'blogflask89@gmail.com'
    MAIL_PASSWORD = 'av8-JJm-JFY-jiS'


class Testing(Config):
    TESTING = True
    DEBUG = True


class Develop(Config):
    TESTING = False
    DEBUG = True


class Production(Config):
    TESTING = False
    DEBUG = False
