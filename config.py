class Config(object):
    # App settings
    SECRET_KEY = None
    SECURITY_PASSWORD_SALT = None
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'main.py'
    RECAPTCHA_PUBLIC_KEY = None
    RECAPTCHA_PRIVATE_KEY = None

    # Mail settings
    MAIL_SERVER = None
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = None
    MAIL_DEFAULT_SENDER = None
    MAIL_PASSWORD = None
    FEEDBACK_MAIL = None

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
