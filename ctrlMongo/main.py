import pymongo
from config import *
from multiprocessing import Pool

client = pymongo.MongoClient(HOST)
db = client[MONGO_DB]
table = db["data"].find()


def switch(table):
    for item in table:
        if item["_id"][:3]=="bao":
            try:
                if db["baoxiaojiongtu"].insert_one(item):
                    print('保存到MONGODB成功！！', item)
            except Exception:
                print('##保存到MONGODB失败###', item)
        elif item["_id"][:3] == "qua":
            try:
                if db["quanqiugaoxiaoGIF"].insert_one(item):
                    print('保存到MONGODB成功！！', item)
            except Exception:
                print('##保存到MONGODB失败###', item)
        elif item["_id"][:3] == "duo":
            try:
                if db["duowanjiongtu"].insert_one(item):
                    print('保存到MONGODB成功！！', item)
            except Exception:
                print('##保存到MONGODB失败###', item)


def main(table):
    switch(table)


if __name__ == "__main__":
    main(table)
