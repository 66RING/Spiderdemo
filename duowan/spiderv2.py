import json
import requests
from config import *
import pymongo
import re
from multiprocessing import Pool

client = pymongo.MongoClient(LOCALHOST)
db = client[MONGO_DB]


def get_page_data(gid):
    # url = "http://tu.duowan.com/index.php?r=show/getByGallery/&gid=139248&_=1565277154640"
    url = "http://tu.duowan.com/index.php?r=show/getByGallery/&gid="+str(gid)
    res = requests.get(url)
    data = json.loads(res.text)
    return data


def save_to_mongo(data):
    table = data.get("gallery_title")
    if 0 <= is_select(table) <= 2:
        id = ""
        if is_select(table) == 0:
            id = "duowanjiongtu"+select_id(table)
        elif is_select(table) == 1:
            id = "quanqiugaoxiaoGIF"+select_id(table)
        elif is_select(table) == 2:
            id = "baoxiaojiongtu"+select_id(table)
        if is_exist(id):
            print("###", table, "已存在###")
        else:
            datalist = []
            for item in data.get("picInfo"):
                result = {
                    "describe": item.get("add_intro"),
                    "url": item.get("url")
                }
                datalist.append(result)
            item_list = {
                "_id": id,
                "title": table,
                "data": datalist
            }
            try:
                if db[MONGO_TABLE].insert_one(item_list):
                    print('保存到MONGODB成功！！', item_list)
            except Exception:
                print('##保存到MONGODB失败###', item_list)


def select_id(table):
    id = re.match('.*?(\d+).*', table)
    return id.group(1)


def is_exist(id):
    if db[MONGO_TABLE].find({"_id": id}):
        return True
    return False


def is_select(title):
    title = title[:4]
    list = ["今日囧图", "全球搞笑", "吐槽囧图"]
    if title == list[0]:
        return 0
    elif title == list[1]:
        return 1
    elif title == list[2]:
        return 2


def main(gid):
    try:
        data = get_page_data(gid)
        save_to_mongo(data)
    except Exception:
        pass


if __name__ == "__main__":
    pool = Pool(processes=5)
    pool.map(main, range(139248, -1, -1))
    # main(139248)
    # gid = 139248
    # while gid >= 138238:
    #     main(gid)
    #     gid -= 1
