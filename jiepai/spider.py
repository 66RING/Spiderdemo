import requests
import time
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from selenium.webdriver.chrome.options import Options
from requests.exceptions import RequestException
from selenium import webdriver
import json
from multiprocessing import Pool
import pymongo
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
chrome_options = Options()
# 添加启动参数
chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# 添加了chrome_options 后则会不显示出Chrome窗口,没有添加的话运行会跳出Chrome窗口
bs = webdriver.Chrome(chrome_options=chrome_options)


def get_page_index(offset):
    cookie = '''tt_webid=6719662733485082120; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=6ywegxy8m1564543407115; tt_webid=6719662733485082120; csrftoken=6e113bace59b52b3b857ed616b47909a; UM_distinctid=16c460dec643ee-08e4c29b018e2e-37607c02-13c680-16c460dec65a8d; CNZZDATA1259612802=1393411661-1564538727-https%253A%252F%252Fwww.toutiao.com%252F%7C1564538727; s_v_web_id=276607d9da58636e1ba2ebfd3f898d88'''
    header = {
        'cookie': cookie
    }
    data = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time()),
        # 'cookie': cookie
        # 'timestamp': 1562932899455
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)
    # broser.get(url)
    response = requests.get(url, headers=header)
    # print(url)
    # print(response.status_code)
    # print(response.text)
    return response.text


def parse_page(res):
    data = json.loads(res)
    for item in data.get('data'):
        # print(item.get('article_url'))
        if item.get('article_url'):
            yield item.get('article_url')


def get_page_detail(url):
    bs.get(url)
    return bs.page_source
    # header = {
    #     # 'upgrade-insecure-requests': '1',
    #     'user-agent':'''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36''',
    # }
    # res = requests.get(url, headers=header)
    # print(res.status_code, res.text)
    # return res.text


def parse_page_detail(html):
    doc = pq(html)
    title = doc.find('h2.title').text()
    if title != '':
        items = doc('li.image-item img').items()
        img = [item.attr('data-src') for item in items]
        data = {
            'title': title,
            'img': img
        }
        print(data)
        return data


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('保存到MONGODB成功！！', result)
    except Exception:
        print("保存失败")



def main(offset):
    res = get_page_index(offset)
    for url in parse_page(res):
        html = get_page_detail(url)
        data = parse_page_detail(html)
        save_to_mongo(data)


if __name__ == '__main__':
    # pool = Pool(processes=5)
    # li = [i*20 for i in range(0, 10)]
    # pool.map(main, li)
    for i in range(0, 10):
        main(i*20)
