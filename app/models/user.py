from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, BigInteger

from app.extension import db, login_manager


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)


class User(db.Model):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键id')
    account = Column(String(20), nullable=False, unique=True, comment='账号/登录名')
    password = Column(String(20), nullable=False, comment='密码')
    tokens = Column(BigInteger, nullable=True, comment='剩余tokens')
    summary_key = Column(String(32), nullable=False, unique=True, comment='后台生成的唯一key')
    openai_key = Column(String(60), nullable=True, comment='openai key')
    active = Column(Boolean, default=True, comment='记录是否有效(1有效，0无效)，逻辑删除标识')
    created_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
