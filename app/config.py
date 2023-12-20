import os

import redis
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
redis_client = redis.Redis(connection_pool=pool)

SUMMARY_PROGRESS_KEY = "summary_progress"


class Config:
    SECRET_KEY = os.environ.get('KEY') or '123456'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL