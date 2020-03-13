import re
import requests
import selenium
import pyquery
import pymysql
import pymongo
import redis
import flask
import django
import jupyter


def get_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
    return None


def get_data(html):
    pattern = re.compile('<dd>.*?title="(.*?)".*?data-src="(.*?)".*?"star">(.*?)</p>.*?"releasetime">(.*?)'
                         '</p>.*?"integer">(.*?)</i>.*?"fraction">(.*?)</i>.*?', re.S)
    result = re.findall(pattern, html)
    with open('list.txt', 'a') as f:
        for item in result:
            f.write(item[0]+'\n')
            f.write(item[1]+'\n')
            f.write(item[2].split()[0]+'\n')
            f.write(item[3]+'\n')
            f.write(item[4]+item[5]+'\n\n')
            f.write('------------------\n')
            print(item[0])
            print(item[1])
            print(item[2].split()[0])
            print(item[3])
            print(item[4], item[5])
        f.close()


def main():
    for offset in range(10):
        url = 'https://maoyan.com/board/4?offset='+str(offset)
        get_data(get_page(url))


if __name__ == '__main__':
    main()
