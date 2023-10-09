from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql

pymysql.install_as_MySQLdb()
db = SQLAlchemy()

login_manager = LoginManager()


def config_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)