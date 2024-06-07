AI文章摘要生成器 server 端

使用的时候需要在项目根目录下创建一个 .env 文件，里面参数 
```
OPENAI_API_KEY = sk-1233332321
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/ai_summary'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD= xxx
```

## Mweb 生成博客使用 ai summary 

### 前提条件
1. 将 server 部署起来，并提供外网域名访问
   1. 部署方式可以选择 python 部署，或者选择 docker 部署。
2. server 地址跟博客地址一级域名保持一致，否则会有跨域问题
3. server 部署好之后，初始化 sql
   1. user 设置 summary_key，随机字符串即可
   2. auth_site 绑定 user_id 并设置自己的域名及缓存小时数



### 使用步骤

操作仅仅2步即可使用。

比如 我使用的是  site-medium-like 这个主题。

1. 在 post.html 中引用 js、css 文件.
    ```javascript
    <link href="https://xxx/static/summary_gpt.css" rel="stylesheet"/>
    <script src="https://xxx/static/summary_gpt.js"></script>
    ```
   也可以将这两个文件上传到 cdn 上。
2. 设置几个参数
    ```javascript
    <script>
        let summary_gpt_article_content_selector= '.article-content';
        let summary_gpt_key = '12345678';
        let summary_gpt_domain = 'http://xxxxx:5000';
    </script>
    ```
   > 参数作用
   >1. summary_gpt_article_content_selector= '.article-content' 
       > 这个 class 就是 Mweb 主题生成的文章内容。server 端会去爬取文章的内容，将内容发送给 openai
   >2. summary_gpt_key  提前设置好的 summary_key
   >3. summary_gpt_domain 就是部署的 server 外网地址

使用 Mweb 生成博客后，这两个文件会自动加载到文章的 html 中。

由于这个主题还引用了 jQuery，所以 js 中的代码会自动执行.
```javascript
$(function () {
  summary_gpt()
});
```

js 代码会创建一个 aiDiv，并且将这个 aiDiv 插到 .article-content class 下的第一个 div 之前。



## api
### GET 流式返回文章摘要

GET /summaryFromUrl

#### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|url|query|string| 是 |none|
|content_div_class|query|string| 是 |none|



### GET 非流式返回文章摘要

GET /summaryFromUrlSync

#### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|url|query|string| 是 |none|
|content_div_class|query|string| 是 |none|




## Docker 部署
`docker build -t summary-gpt-server .`

`docker run -d -p 5000:5000 --name summary-gpt-server summary-gpt-server`



## docker compose

`docker-compose up -d`
