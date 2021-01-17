# -*- coding: utf-8 -*-
from defines import *
from PyQt5 import QtCore, QtGui, QtWidgets

from .widget import CInterface



import math
import globals
_translate = QtCore.QCoreApplication.translate

class CViewMenuBar(QtWidgets.QMenuBar, CInterface):
    def __init__(self, parent, MainWindow):
        super().__init__(parent)
        self.init_menu(MainWindow)

    
    def init_menu(self, MainWindow):
        self.menu_file= QtWidgets.QMenu(self)
        self.menu_file.setObjectName("file")
        self.menu_config = QtWidgets.QMenu(self)
        self.menu_config.setObjectName("config")

        self.menu_file.setTitle(_translate("MainWindow", "文件"))
        self.menu_config.setTitle(_translate("MainWindow", "配置"))

        self.init_action(MainWindow)

        self.addAction(self.menu_file.menuAction())
        self.addAction(self.menu_config.menuAction())

        MainWindow.setMenuBar(self)

        self.triggered.connect(self.OnActionTrigged)


    def init_action(self, MainWindow):
        self.action_load_config = QtWidgets.QAction(MainWindow)
        self.action_load_config.setObjectName("action_load_config")
        self.action_modiy_config = QtWidgets.QAction(MainWindow)
        self.action_modiy_config.setObjectName("action_modiy_config")
        self.action_load_config.setText(_translate("MainWindow", "载入配置"))
        self.action_modiy_config.setText(_translate("MainWindow", "修改配置"))

        self.menu_config.addAction(self.action_load_config)
        self.menu_config.addAction(self.action_modiy_config)




    def OnActionTrigged(self, action):
        name = action.objectName()
        func =  getattr(self, "onActionTrigged_"+name, None)
        if not func :
            return
        
        func()


    def onActionTrigged_action_modiy_config(self):
        config = globals.get_obj("Config")
        config.show_dialog()



    