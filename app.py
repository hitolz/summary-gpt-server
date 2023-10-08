from flask import Flask, Response, render_template,request,jsonify
import openai_api as api
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import re
import util


app = Flask(__name__)
CORS(app)

static_pattern = r"\.(css|js)$"


@app.route('/')
def index():
    return render_template("article.html")


@app.route('/test')
def stream_data():
    return render_template("index.html")


def buildSseResponse(content):
    msg = f"data: {content}\n\n"
    return Response(msg, mimetype='text/event-stream')

@app.before_request
def before_request():
    ip,url =  get_ip_and_url()
    if re.search(static_pattern,url):
        return 
    if request.url_rule.rule == '/summaryFromUrl':
        key = request.args.get('key')
        if not key:
            error_message = '参数 key 为空，请升级 js 版本'
            return buildSseResponse(error_message)
        elif key == '123456':
            error_message = '参数 key 为 123456，请修改为自己的 key。'
            return buildSseResponse(error_message)

    print("before ip:"+ip)
    print("before url:" + url)

def get_ip_and_url():
    ip = request.remote_addr
    url = request.url
    return ip,url



@app.route('/summaryFromContent')
def summaryFromContent():
    content = request.args.get('content')
    return Response(summary_stream(content), mimetype='text/event-stream')

def summary_stream(content):
        for response in api.summary_stream(content):
            yield response

@app.route('/summaryFromUrl')
def summaryFromUrl():
    url = request.args.get('url')
    content_class = request.args.get('content_div_class')
    content = scrape_article(url,content_class)
    return Response(summary_stream(content), mimetype='text/event-stream')


@app.route('/summaryFromUrlSync')
def summaryFromUrlSync():
    url = request.args.get('url')
    content_class = request.args.get('content_div_class')
    content = scrape_article(url,content_class)
    return api.summary(content)


def scrape_article(url,content_class):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content,'html.parser')

        content = soup.find('div',class_=content_class).get_text()
        return content
    else:
        print("请求失败")
        return None


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
