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
import mail_box





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
    dbobj = globals.get_obj("dbobj")
    for v in COLLECTION.values():
        ret = dbobj.CreateIndex(v[0], v[1])

def init_mail():
    config = globals.get_obj("config")
    mail_data = config["mail"]
    obj = mail_box.CMailBox(mail_data["user"], mail_data["password"], mail_data["host"])
    obj.SetSender(mail_data["user"])
    for name in mail_data["to"]:
        obj.SetReceive(name)
    globals.set_obj("mail", obj)


# def test():
#     test = False
#     ls = ["000001", "006482","213917", "002937","010270"]
#     f = fund_api.spiker_fund_and_save
#     f= fund_api.load_fund
#     if test :
#         for i in ls:
#             f(i)
#     else:
#         ret = f("000001")
#         data = ret["data"]["total"]["net_worth"]
#         print("data:",data)
#         x = []
#         y = []
#         x1= []
#         y1 = []
#         for v in data:
#             x.append(v[0]/1000)
#             y.append(v[1])
#             y1.append(v[1]+0.5)
#         plt.figure()
#         plt.rcParams['font.family']=['STFangsong']
#         plt.title("净值走势") 
#         plt.xlabel("年份")
#         plt.ylabel("净值")
#         plt.plot(x,y,"r")
#         plt.plot(x,y1,"g")
#         plt.show()
        

def main():
    #读取配置
    init_config()
    #初始化db
    init_db()
    #建立索引
    init_db_index()
    #初始化邮件对象
    init_mail()
    t = time.time()
    mail_box.test()
    print("user:",time.time()- t)

  



if __name__ == "__main__":
    main()