import re

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, Response, render_template, request

import openai_api as api
from app.config import redis_client
from app.extension import db
from app.models.user import User

ai_summary = Blueprint('admin', __name__)

static_pattern = r"\.(css|js)$"


@ai_summary.route('/article')
def index():
    return render_template("article.html")


@ai_summary.route('/test')
def stream_data():
    return render_template("index.html")


def build_sse_response(content):
    msg = f"data: {content}\n\n"
    return Response(msg, mimetype='text/event-stream')


@ai_summary.before_request
def before_request():
    ip, url = get_ip_and_url()
    if re.search(static_pattern, url):
        return
    if request.url_rule.rule == '/summaryFromUrl':
        key = request.args.get('key')
        if not key:
            error_message = '参数 key 为空，请升级 js 版本'
            return build_sse_response(error_message)
        elif key == '123456':
            error_message = '参数 key 为 123456，请修改为自己的 key。'
            return build_sse_response(error_message)

    print("before ip:" + ip)
    print("before url:" + url)


def get_ip_and_url():
    ip = request.remote_addr
    url = request.url
    return ip, url


@ai_summary.route('/summaryFromContent')
def summaryFromContent():
    content = request.args.get('content')
    return Response(summary_stream(content, key=None), mimetype='text/event-stream')


def summary_stream(content, key):
    if key:
        exist = redis_client.set(key, '', nx=True)
        if exist:
            redis_client.set(key, '', ex=86400)
            return
    for response in api.summary_stream(content):
        print(response)
        if key:
            redis_client.append(key, response)
        yield response


def find_cache(url):
    print("url = " + url)
    # cache = ArticleCache.query.filter(ArticleCache.url == url).order_by(desc("id")).first()
    cache = redis_client.get(url)
    if cache:
        print("cache " + cache)
        return cache
    return None


@ai_summary.route('/summaryFromUrl')
def summaryFromUrl():
    url = request.args.get('url')
    cache = find_cache(url)
    if cache:
        return Response(cache)
    content_class = request.args.get('content_div_class')
    content = scrape_article(url, content_class)
    return Response(summary_stream(content, url), mimetype='text/event-stream')


@ai_summary.route('/summaryFromUrlSync')
def summaryFromUrlSync():
    url = request.args.get('url')
    content_class = request.args.get('content_div_class')
    content = scrape_article(url, content_class)
    return api.summary(content)


def scrape_article(url, content_class):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        content = soup.find('div', class_=content_class).get_text()
        return content
    else:
        print("请求失败")
        return None


@ai_summary.route('/user')
def user_list():
    users = db.session.execute(db.select(User).order_by(User.account)).scalars()
    return render_template("user/list.html", users=users)
