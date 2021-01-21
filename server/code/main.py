# -*- coding: utf-8 -*-
import sys
import os
libpath = os.path.abspath("./lib")
sys.path.append(libpath)

from defines import *

import globals
import mongo_api
import config_api

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


def main():
    init_config()
    init_db()
    # obj = mongo_api.CMongodbManager("_game", "192.168.6.108", "27017")
    # globals.set_obj("gamedb", obj)



if __name__ == "__main__":
    main()