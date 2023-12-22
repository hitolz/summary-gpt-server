from datetime import datetime, timedelta
from urllib.parse import urlparse

import pytz
from sqlalchemy import desc, text

from app import openai_api
from app.config import redis_client
from app.extension import db
from app.models.article_cache import ArticleCache
# 获取北京时区
from app.models.auth_site import AuthSite

beijing_tz = pytz.timezone('Asia/Shanghai')


def find_cache(url):
    print("url = " + url)
    cache = ArticleCache.query.filter(ArticleCache.url == url, ArticleCache.active == 1).order_by(desc("id")).first()
    if cache:
        return cache.summary_content
    return None


def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


def get_auth_site(key, current_app):
    sql = text("""select a.* from auth_site a join `user`  b on a.user_id = b.id where b.summary_key = :summary_key""")
    result = db.session.execute(sql, {'summary_key': key}).fetchall()
    return result


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
            expire_time=get_expire_time(key, current_app)
        )
        with current_app.app_context():
            cache.save()
        redis_client.delete(key)


def get_expire_time(key, current_app):
    domain = get_domain(key)
    with current_app.app_context():
        auth_site = AuthSite.query.filter(AuthSite.site_domain == domain, AuthSite.active == 1).first()
        if auth_site:
            return datetime.now(beijing_tz) + timedelta(hours=auth_site.expire_hours)
        return datetime.now(beijing_tz) + timedelta(hours=3)
