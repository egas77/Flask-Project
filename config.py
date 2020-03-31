class Config(object):
    SECRET_KEY = 'LMTk06lLwpD4HlZl'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static\\db\\db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'main.py'
    RECAPTCHA_PUBLIC_KEY = '6LdyceUUAAAAAHNV2E4yIDNK3sS-vZe5KqJw4RIk'
    RECAPTCHA_PRIVATE_KEY = '6LdyceUUAAAAAARkkR8_ZIFQPaLLiFc3y9CWYvZj'


class Develop(Config):
    TESTING = True
    DEBUG = True


class Production(Config):
    DEBUG = False
