import re

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, Response, render_template, request
from flask import current_app

from app.extension import db
from app.models.user import User
from app.services import find_cache, summary_stream

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


@ai_summary.route('/summaryFromUrl')
def summaryFromUrl():
    url = request.args.get('url')
    cache = find_cache(url)
    if cache:
        return Response(cache, mimetype='text/event-stream')
    content_class = request.args.get('content_div_class')
    content = scrape_article(url, content_class)
    return Response(summary_stream(content, url, current_app._get_current_object()), mimetype='text/event-stream')


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
