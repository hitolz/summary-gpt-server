from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func

from app.extension import db


class ArticleCache(db.Model):
    __tablename__ = 'article_cache'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(1024), nullable=False, comment='文章链接')
    summary_content = Column(Text, comment='摘要内容')
    active = Column(Boolean, default=True, comment='记录是否有效(1有效，0无效)，逻辑删除标识')
    created_time = Column(DateTime, default=func.now(), comment='创建时间')
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
    expire_time = Column(DateTime, comment='过期时间')

    def save(self):
        db.session.add(self)
        db.session.commit()
