from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extension import db


class ArticleCache(db.Model):
    __tablename__ = "article_cache"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String)
    summary_content: Mapped[str] = mapped_column(String)