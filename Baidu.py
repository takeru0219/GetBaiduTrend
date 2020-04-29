import slackweb
from bs4 import BeautifulSoup
import requests
slack_url = '' # incoming webhook

# 取得 -> BeautifulSoupに渡す
url = 'http://top.baidu.com/buzz?b=341&fr=topbuzz_b342'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# soup内の処理
data_array_keyword = soup.find_all(class_ = 'list-title')
data_array_score = soup.find_all(class_ = 'last')

words = []
urls = []
scores = []

for keyword_url, score in zip(data_array_keyword[0:10], data_array_score[2:12]):
    words.append(keyword_url.text)
    urls.append(keyword_url.get('href'))
    scores.append(score.text.strip())

# Slackに流す
slack = slackweb.Slack(url = slack_url)
attachments = []

for word, url, score in zip(words, urls, scores):
    if int(score) >= 100000:
        color = 'danger'
    elif int(score) >= 40000:
        color = 'warning'
    else:
        color = 'good'
    attachments.append(
    {
        # 'fallback' : '今日热点事件排行榜',
        'title' : word,
        'title_link' : url,
        'text' : score,
        'color' : color
    })

slack.notify(
    text = '今日热点事件排行榜', 
    username = '百度热点',
    attachments = attachments
)
