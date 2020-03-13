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
from multiprocessing import Pool



def get_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.text
    return None


def get_data(html):
    catch = re.compile('<ul>(.*?)</ul>.*?', re.S)
    html = re.findall(catch, html)[0]

    pattern = re.compile('<li>.*?<span class="emoji">(.*?)</span>\s(.*?)<.*?', re.S)
    result = re.findall(pattern, html)
    with open('list.txt', 'a') as f:
        for item in result:
            f.write(item[0]+'\t'+item[1]+'\n')
            print(item[0]+'\t'+item[1]+'\n')
        f.close()

def fail_list(v):
    with open('fail_list.txt', 'a') as f:
        f.write(v+'\n')
        print('###fail###  -->  '+v+'\n')
        f.close()



def main(v):
    try:
        html = get_page("https://emojipedia.org/unicode-"+v+"/")
        get_data(html)
    except Exception:
        fail_list(v)



if __name__ == "__main__":
    list = ['1.1','3.0','3.1','3.2','4.0','4.1','5.0','5.1','5.2','6.0','6.1','7.0','8.0','9.0','10.0','11.0','12.0','13.0']
    pool = Pool(processes=5)
    pool.map(main, list)

