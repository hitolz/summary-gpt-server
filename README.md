AI文章摘要生成器 server 端

使用的时候需要在项目根目录下创建一个 .env 文件，里面只有一个参数 OPENAI_API_KEY

针对 Mweb 生成的博客制作，content_div_class=article-content

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


