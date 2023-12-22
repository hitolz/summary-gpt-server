from sqlalchemy import Column, String, Boolean, DateTime, func, BigInteger, Integer

from app.extension import db


class AuthSite(db.Model):
    __tablename__ = 'auth_site'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键id')
    user_id = Column(BigInteger, nullable=False, comment='用户id')
    site_domain = Column(String(100), nullable=False, comment='网站域名')
    site_summary_key = Column(String(10), nullable=True, comment='网站对应的key')
    active = Column(Boolean, default=True, comment='记录是否有效(1有效，0无效)，逻辑删除标识')
    created_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
    expire_hours = Column(Integer, nullable=False, comment='缓存小时数')
