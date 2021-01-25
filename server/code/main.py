# -*- coding: utf-8 -*-
import sys
import os
#公共库
libpath = os.path.abspath("./lib")
sys.path.append(libpath)

from defines import *

import time

import global_obj
import mongo_api
import config_api
import spiker.fund_api as fund_api
import mail_box
import logger
import task
import log
import myfund


def init_config():
    file = CONFIG_FILE
    data = config_api.load_config(file)
    #obj = config_api.CConfig(data)
    global_obj.set_obj("config", data)



def init_db():
    config = global_obj.get_obj("config")
    db_data = config["db"]
    obj = mongo_api.CMongodbManager(DB_NAME, db_data["addr"], db_data["port"], db_data["user"], db_data["password"])
    global_obj.set_obj("dbobj", obj)

def init_db_index():
    dbobj = global_obj.get_obj("dbobj")
    for v in COLLECTION.values():
        ret = dbobj.CreateIndex(v[0], v[1])





def main():
    #读取配置
    init_config()
    #初始化日志
    logger.init_logger()
    #初始化db
    init_db()
    #建立索引
    init_db_index()
    #初始化邮件对象
    mail_box.init_mail()
    #初始化定时任务
    task.init_task()

    #添加任务
    myfund.init_fund_task()
    
    #开始执行任务
    taskobj = global_obj.get_obj("task_timer")
    taskobj.RunForever()

    


  



if __name__ == "__main__":
    main()