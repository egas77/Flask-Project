class Config(object):
    SECRET_KEY = 'LMTk06lLwpD4HlZl'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'main.py'
    RECAPTCHA_PUBLIC_KEY = '6LdyceUUAAAAAHNV2E4yIDNK3sS-vZe5KqJw4RIk'
    RECAPTCHA_PRIVATE_KEY = '6LdyceUUAAAAAARkkR8_ZIFQPaLLiFc3y9CWYvZj'

    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'flask-blog@yandex.ru'
    MAIL_DEFAULT_SENDER = 'flask-blog@yandex.ru'
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
