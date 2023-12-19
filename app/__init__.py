from flask import Flask
from flask_cors import CORS

from app.api import config_blueprint
from app.config import Config
from app.extension import config_extensions


def creat_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    config_extensions(app)
    config_blueprint(app)
    return app
