import json
import requests
import os
import datetime
from datetime import timedelta

def get_data(URL):
    response = requests.get(url=URL)
    data = response.json()
    return data

def parse_data(data):
    lst = []
    for it in data['items']:
        # only fetch today's news
        print(it['item']['dateUpdated'][0:10])
        us_day = datetime.datetime.now() - timedelta(days=1)
        if it['item']['dateUpdated'][0:10] == us_day.strftime('%Y-%m-%d'):
            lst.append(it['item'])
    feishu_content = []
    for l in lst:
        content = [{
            'tag': 'text',
            'text': l['additionalFields']['headline']
        },{
            'tag': 'a',
            'text': 'link',
            'href': 'https://aws.amazon.com/%s' % l['additionalFields']['headlineUrl']
        }]
        feishu_content.append(content)
    return {
        'msg_type': "post",
        'content': {
            'post': {
                'zh-cn': {
                    'title': "AWS What's New %s" % datetime.datetime.now().strftime('%Y-%m-%d'),
                    'content': feishu_content
                }
            }
        }
    }


def post_data(data, URL):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=URL, json=data, headers=headers)
    return response    

def lambda_handler(event, context):
    
    URL = os.environ.get('URL', 'https://aws.amazon.com/api/dirs/items/search?item.directoryId=whats-new-v2&sort_by=item.additionalFields.postDateTime&sort_order=desc&size=30&item.locale=en_US')
    if URL:
        data = get_data(URL)
        feishu_msg = parse_data(data)
        print(feishu_msg)
        feishu_url = os.environ.get('FEISHU_URL', 'https://open.feishu.cn/open-apis/bot/v2/hook/b3435517-5d71-496b-a289-1c6aaad1862f')
        resp = post_data(feishu_msg, feishu_url)
        print(resp.text)

    return {
        'status': 200
    }

