import json
import requests
from config import *
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient(HOST, connect=False)
db = client[MONGO_DB]


def get_page_data(gid):
    # url = "http://tu.duowan.com/index.php?r=show/getByGallery/&gid=139248&_=1565277154640"
    url = "http://tu.duowan.com/index.php?r=show/getByGallery/&gid="+str(gid)
    res = requests.get(url)
    data = json.loads(res.text)
    return data


def save_to_mongo(data):
    table = data.get("gallery_title")
    if is_exist(table):
        print("###", table, "已存在###")
    elif is_select(table):
        for item in data.get("picInfo"):
            result = {
                "describe": item.get("add_intro"),
                "url": item.get("url")
            }
            try:
                if db[table].insert_one(result):
                    print('保存到MONGODB成功！！', result)
            except Exception:
                print('##保存到MONGODB失败###', result)


def is_exist(name):
    if name in db.list_collection_names():
        return True
    return False


def is_select(title):
    title = title[:4]
    list = ["今日囧图", "全球搞笑", "吐槽囧图"]
    if title in list:
        return True
    return False


def main(gid):
    try:
        data = get_page_data(gid)
        save_to_mongo(data)
    except Exception:
        pass


if __name__ == "__main__":
    pool = Pool(processes=5)
    pool.map(main, range(139248, -1, -1))
    # gid = 139248
    # while gid >= 138238:
    #     main(gid)
    #     gid -= 1
