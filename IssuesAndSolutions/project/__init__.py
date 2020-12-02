
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    db_path = os.path.join(os.path.dirname(__file__), 'db2.sqlite')
    sqlite_db_uri = 'sqlite:///{}'.format(db_path)

    ## Set up MySQL server on AWS or HEROKU update with new table
    db_username = "username"
    db_pass     = "pass"
    db_host     = "host"
    db_db       = "database"
    mysql_db_uri = "mysql+pymysql://{}:{}@{}/{}".format(db_username, db_pass, db_host, db_db) 

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    ## Setting up AWS RDS MySQL database service
    db2_username = "username"
    db2_pass = "pass"
    db2_host = "host"
    db2_db = "databse"
    AWS_mysql_db_uri = "mysql+pymysql://{}:{}@{}/{}".format(db2_username, db2_pass, db2_host, db2_db)

    app.config['SQLALCHEMY_DATABASE_URI'] = AWS_mysql_db_uri or mysql_db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_POOL_RECYCLE']=90

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        #
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

from . import errors