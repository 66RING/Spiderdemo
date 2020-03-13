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
    if is_select(table):
        id = ""
        if is_select(table) == "duowanjiongtu":
            id = "duowanjiongtu"+select_id(table)
        elif is_select(table) == "quanqiugaoxiaoGIF":
            id = "quanqiugaoxiaoGIF"+select_id(table)
        elif is_select(table) == "baoxiaojiongtu":
            id = "baoxiaojiongtu"+select_id(table)
        if not is_exist(id, is_select(table)):
            print("###", is_select(table), "已存在###")
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
                if db[is_select(table)].insert_one(item_list):
                    print('保存到MONGODB成功！！', item_list)
            except Exception:
                print('##保存到MONGODB失败###', item_list)


def select_id(table):
    id = re.match('.*?(\d+).*', table)
    return id.group(1)


def is_exist(id, table):
    if db[table].find({"_id": id}):
        return True
    return False


def is_select(title):
    title = title[:4]
    list = ["今日囧图", "全球搞笑", "吐槽囧图"]
    if title == list[0]:
        return "duowanjiongtu"
    elif title == list[1]:
        return "quanqiugaoxiaoGIF"
    elif title == list[2]:
        return "baoxiaojiongtu"


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
