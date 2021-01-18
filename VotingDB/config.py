class Config(object):
    DEBUG = False
    TESTING = False

    db_username = "#"
    db_pass     = "#"
    db_host     = "#"
    db_db       = "#"
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(db_username, db_pass, db_host, db_db)
    SQLALCHEMY_TRACK_MODIFICATIONS = None
    SECRET_KEY   = "#"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True