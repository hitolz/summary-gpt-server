import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS

from app.api import config_blueprint
from app.config import Config
from app.extension import config_extensions
from app.services.task import cache_expire


def creat_app():
    app = Flask(__name__)
    # 设置日志记录器
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    CORS(app)
    app.config.from_object(Config)
    config_extensions(app)
    config_blueprint(app)
    scheduler = BackgroundScheduler()
    # scheduler.add_job(func=cache_expire, args=(app,), trigger='interval', seconds=2)
    scheduler.add_job(func=cache_expire, args=(app,), trigger='cron', minute=0)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return app
