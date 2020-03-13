from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 200)


def search():
    browser.get('https://www.jd.com/')
    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#key")))
    input.send_keys('美食')
    sumit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > div > div.form > button")))
    sumit.click()
    toltal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1) > b")))
    return int(toltal.text)


def get_product():
    js = "var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)
    time.sleep(3)
    html = browser.page_source
    doc = pq(html)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > input")))
    items = doc('li.gl-item').items()
    for item in items:
        product = {
            # 'img': item.find('div.p-img a img').attr('src'),
            'price': item.find('.p-price i').text(),
            'name': item.find('.p-name a').attr('title'),
            'comment': item.find('div div strong a').text(),
            'shop': item.find('.p-shop a').text()

        }
        print(product)
        save_to_mongo(product)


def next_page(page_num):
    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > input")))
    input.clear()
    input.send_keys(page_num)
    sumit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > a")))
    sumit.click()


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('保存到MONGODB成功！！', result)
    except Exception:
        print("保存失败")


def main():
    toltal = search()
    print(toltal)
    for i in range(2, toltal+1):
        get_product()
        try:
            next_page(i)
        except Exception:
            next_page(i)


if __name__ == '__main__':
    main()