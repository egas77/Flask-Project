class Config(object):
    SECRET_KET = 'LMTk06lLwpD4HlZl'


class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
