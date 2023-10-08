from flask import Flask

from app import config
from app.api import config_blueprint
from app.extension import config_extensions

from manage import config_name


def creat_app(DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    config_extensions(app)
    config_blueprint(app)
    return app

