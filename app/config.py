import os

import redis
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
redis_client = redis.Redis(connection_pool=pool)

SUMMARY_PROGRESS_KEY = "summary_progress"

class Config:
    SECRET_KEY = os.environ.get('KEY') or '123456'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
#
# class DevelopmentConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:12345678@localhost:3306/ai_summary'
#
# class TestingConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/test-database'
#
# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/product-database'
#
#
# # 生成一个字典，用来根据字符串找到对应的配置类
# config = {
#     "development": DevelopmentConfig,
#     "testing": TestingConfig,
#     "production": ProductionConfig,
#     "default": DevelopmentConfig
# }
