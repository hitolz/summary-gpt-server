from flask import Flask

from app.config import config
from app.api import config_blueprint
from app.extension import config_extensions

from flask_cors import CORS


def creat_app(config_name):
    app = Flask(__name__)
    CORS(app)
    # app.config.from_object(config.get(config_name))
    # config_extensions(app)
    config_blueprint(app)
    return app
