from datetime import datetime

from app.extension import db
from app.models.article_cache import ArticleCache


def cache_expire(app):
    app.logger.info("cache expire job executing...")
    with app.app_context():
        cache_article = ArticleCache.query.filter(ArticleCache.active == 1,
                                                  ArticleCache.expire_time < datetime.now()).all()
        app.logger.info("expire articles count = " + str(len(cache_article)))
        if cache_article:
            for article in cache_article:
                app.logger.info("expire article cache url = " + article.url)
                article.active = 0
            db.session.commit()
