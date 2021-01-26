# -*- coding: utf-8 -*-
import sys

import os


libpath = os.path.abspath("./lib")
sys.path.append(libpath)

from defines import *

from PyQt5 import QtWidgets, QtGui,QtCore
from override.oui_main import Oui_MainWindow
from view import Ui_fund_view



import spiker_api
import global_obj
import log
import time
import config_api
import mongo_api

def init_config(config_file = None):
    file = config_file if config_file else CONFIG_FILE
    data = config_api.load_config(file)
    global_obj.set_obj("config", data)

def init_db():
    config = global_obj.get_obj("config")
    db_data = config["db"]
    obj = mongo_api.CMongodbManager(DB_NAME, db_data["addr"], db_data["port"], db_data["user"], db_data["password"])
    global_obj.set_obj("dbobj", obj)

def init_App():
    app = QtWidgets.QApplication(sys.argv)
    global_obj.set_obj("App", app)
    mainwindow = Oui_MainWindow()
    global_obj.set_obj("MainWindow", mainwindow)
    return app, mainwindow


def main():

    init_config()
    init_db()
    
    app,mainwindow = init_App()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    