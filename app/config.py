import os

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


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
