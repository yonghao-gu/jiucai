# -*- coding: utf-8 -*-
import sys
import os
libpath = os.path.abspath("./lib")
sys.path.append(libpath)

from defines import *

import time

import globals
import mongo_api
import config_api
import spiker.fund_api as fund_api


def init_config():
    file = CONFIG_FILE
    data = config_api.load_config(file)
    #obj = config_api.CConfig(data)
    globals.set_obj("config", data)



def init_db():
    config = globals.get_obj("config")
    db_data = config["db"]
    obj = mongo_api.CMongodbManager(DB_NAME, db_data["addr"], db_data["port"], db_data["user"], db_data["password"])
    globals.set_obj("dbobj", obj)


def init_db_index():
    pass

def test():
    test = True
    ls = ["000001", "006482","213917", "002937","010270"]
    f = fund_api.spiker_fund_and_save
    if test :
        for i in ls:
            f(i)
    else:
        f("000001")

def main():
    #读取配置
    init_config()
    #初始化db
    init_db()
    #建立索引
    init_db_index()
    t = time.time()
    test()
    print("user:",time.time()- t)

  



if __name__ == "__main__":
    main()