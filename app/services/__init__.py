from datetime import datetime, timedelta

import pytz
from sqlalchemy import desc

from app import openai_api
from app.config import redis_client
from app.models.article_cache import ArticleCache

# 获取北京时区
beijing_tz = pytz.timezone('Asia/Shanghai')


def find_cache(url):
    print("url = " + url)
    cache = ArticleCache.query.filter(ArticleCache.url == url, ArticleCache.active == 1).order_by(desc("id")).first()
    if cache:
        return cache.summary_content
    return None


def summary_stream(content, key, current_app):
    not_exist = redis_client.set(key, '', nx=True)
    if not_exist:
        redis_client.set(key, '', ex=300)

    for response in openai_api.summary_stream(content, key):
        print(response)
        if not_exist:
            redis_client.append(key, response)
        yield response

    if not_exist:
        cache_content = redis_client.get(key)
        cache = ArticleCache(
            url=key,
            summary_content=cache_content,
            active=1,
            expire_time=datetime.now(beijing_tz) + timedelta(hours=3)
        )
        with current_app.app_context():
            cache.save()
        redis_client.delete(key)
