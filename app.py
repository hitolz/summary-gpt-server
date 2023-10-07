from flask import Flask, Response, render_template,request
import openai_api as api
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template("article.html")



@app.route('/test')
def stream_data():
    return render_template("index.html")


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
