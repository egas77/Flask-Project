class Config(object):
    # App settings
    SECRET_KEY = 'LMTk06lLwpD4HlZl'
    SECURITY_PASSWORD_SALT = 'iZRMbSOFBYu4xoOW'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'main.py'
    RECAPTCHA_PUBLIC_KEY = '6LfcguUUAAAAAMWvFiu8rpazGR61ZxuIDbtkaG65'
    RECAPTCHA_PRIVATE_KEY = '6LfcguUUAAAAAEWzpN78kxcUj31kU8FAuQn2UG8S'

    # Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'blogflask89@gmail.com'
    MAIL_DEFAULT_SENDER = 'blogflask89@gmail.com'
    MAIL_PASSWORD = 'av8-JJm-JFY-jiS'
    FEEDBACK_MAIL = 'ebedak2003@yandex.ru'

    # User settings
    POSTS_ON_PAGE = 5
    COMMENTS_ON_PAGE = 10
    USERS_ON_PAGE = 20
    POSTS_ON_USER_PAGE = 10


class Testing(Config):
    TESTING = True
    DEBUG = True


class Develop(Config):
    TESTING = False
    DEBUG = True


class Production(Config):
    TESTING = False
    DEBUG = False
