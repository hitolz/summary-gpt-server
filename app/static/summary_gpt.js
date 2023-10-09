console.log("\n %c 专为Mweb博客文章打造的AI生成摘要工具，如果你也需要，请联系:1126031033@qq.com %c \n", "color: #fadfa3; background: #030307; padding:5px 0;", "background: #fadfa3; padding:5px 0;")

var url = window.location.href;
console.log(url);

function removeTrailingSpace(str) {
  if (str[str.length - 1] === ' ') {
    return str.slice(0, -1);
  }
  return str;
}


function summary_gpt() {
  console.log("summary start...");

  const article_div = document.querySelector(summary_gpt_article_content_selector);

  // 创建要插入的HTML元素
  const aiDiv = document.createElement('div');
  aiDiv.className = 'summary-gpt';

  const aiTitleDiv = document.createElement('div');
  aiTitleDiv.className = 'summary-gpt-title';
  aiDiv.appendChild(aiTitleDiv);

  const aiIcon = document.createElement('i');
  aiIcon.className = 'summary-gpt-title-icon';
  aiTitleDiv.appendChild(aiIcon);

  // 插入 SVG 图标
  aiIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="48px" height="48px" viewBox="0 0 48 48">
        <title>机器人</title>
        <g id="&#x673A;&#x5668;&#x4EBA;" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
          <path d="M34.717885,5.03561087 C36.12744,5.27055371 37.079755,6.60373651 36.84481,8.0132786 L35.7944,14.3153359 L38.375,14.3153359 C43.138415,14.3153359 47,18.1768855 47,22.9402569 L47,34.4401516 C47,39.203523 43.138415,43.0650727 38.375,43.0650727 L9.625,43.0650727 C4.861585,43.0650727 1,39.203523 1,34.4401516 L1,22.9402569 C1,18.1768855 4.861585,14.3153359 9.625,14.3153359 L12.2056,14.3153359 L11.15519,8.0132786 C10.920245,6.60373651 11.87256,5.27055371 13.282115,5.03561087 C14.69167,4.80066802 16.024865,5.7529743 16.25981,7.16251639 L17.40981,14.0624532 C17.423955,14.1470924 17.43373,14.2315017 17.43948,14.3153359 L30.56052,14.3153359 C30.56627,14.2313867 30.576045,14.1470924 30.59019,14.0624532 L31.74019,7.16251639 C31.975135,5.7529743 33.30833,4.80066802 34.717885,5.03561087 Z M38.375,19.4902885 L9.625,19.4902885 C7.719565,19.4902885 6.175,21.0348394 6.175,22.9402569 L6.175,34.4401516 C6.175,36.3455692 7.719565,37.89012 9.625,37.89012 L38.375,37.89012 C40.280435,37.89012 41.825,36.3455692 41.825,34.4401516 L41.825,22.9402569 C41.825,21.0348394 40.280435,19.4902885 38.375,19.4902885 Z M14.8575,23.802749 C16.28649,23.802749 17.445,24.9612484 17.445,26.3902253 L17.445,28.6902043 C17.445,30.1191812 16.28649,31.2776806 14.8575,31.2776806 C13.42851,31.2776806 12.27,30.1191812 12.27,28.6902043 L12.27,26.3902253 C12.27,24.9612484 13.42851,23.802749 14.8575,23.802749 Z M33.1425,23.802749 C34.57149,23.802749 35.73,24.9612484 35.73,26.3902253 L35.73,28.6902043 C35.73,30.1191812 34.57149,31.2776806 33.1425,31.2776806 C31.71351,31.2776806 30.555,30.1191812 30.555,28.6902043 L30.555,26.3902253 C30.555,24.9612484 31.71351,23.802749 33.1425,23.802749 Z" id="&#x5F62;&#x72B6;&#x7ED3;&#x5408;" fill="#444444" fill-rule="nonzero"></path>
        </g>
        </svg>`;

  const aiTitleTextDiv = document.createElement('div');
  aiTitleTextDiv.className = 'summary-gpt-title-text';
  aiTitleTextDiv.textContent = 'AI摘要';
  aiTitleDiv.appendChild(aiTitleTextDiv);

  const aiExplanationDiv = document.createElement('div');
  aiExplanationDiv.className = 'summary-gpt-explanation';
  aiDiv.appendChild(aiExplanationDiv); // 将 tianliGPT-explanation 插入到 aiDiv，而不是 aiTitleDiv


  article_div.insertBefore(aiDiv, article_div.firstChild);

  const element = document.querySelector(".summary-gpt-explanation");

  const apiUrl = `${summary_gpt_domain}/summaryFromUrl?url=${encodeURIComponent(url)}&key=${encodeURIComponent(summary_gpt_key)}&content_div_class=article-content`;
  const eventSource = new EventSource(apiUrl);

  
  eventSource.onmessage = function (event) {
    const data = removeTrailingSpace(event.data);
    // 处理接收到的数据
    element.innerHTML += data
  };

  eventSource.onerror = function (error) {
    // 处理错误
    console.error('EventSource error:', error);
    eventSource.close(); // 停止接收数据并关闭连接
  };

}
$(function () {
  summary_gpt()
});