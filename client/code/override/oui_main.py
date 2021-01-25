# -*- coding: utf-8 -*-

from defines import *

from PyQt5 import QtCore, QtGui, QtWidgets
#from view import Ui_MainWindow
from view import Ui_fund_view
from view import Ui_log_view
from view import Ui_MainWindow
from components import CViewMenu, CViewLog,CViewMenuBar,CViewTest

import global_obj
import log

class Oui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("韭菜收割机")
        self.resize(MainWindowWidth,MainWindowHeight)
        self.setMinimumSize(QtCore.QSize(MainWindowWidth,MainWindowHeight))
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralframe")
        self.setCentralWidget(self.centralwidget)
        self.setWindowIcon(QtGui.QIcon("resource/main_icon.jpg"))

        self.menu = CViewMenuBar(self,self)
        
        self.menu_tree = CViewMenu(self.centralwidget,self)


        self.init_fund_spiker_ui()
        self.init_data_analyse()
        self.init_log_view()
        self.init_test_view()

        #注册事件
        self.menu_tree.clicked.connect(self.on_menu_tree_click)
        #self.menu.triggered.connect(self.on_menu_triggered)

    

        
    def init_fund_spiker_ui(self):
        self.init_fund_ui = QtWidgets.QWidget(self.centralwidget)
        self.init_fund_ui.resize(300,600)
        self.init_fund_ui.move(Divide,0)
        button = QtWidgets.QPushButton()
        button.setText("我是爬虫窗口")
        lable = QtWidgets.QLabel()
        lable.setText("看他")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(lable)
        self.init_fund_ui.setLayout(layout)
        self.init_fund_ui.hide()



    def init_data_analyse(self):
        self.init_data_ui = QtWidgets.QWidget(self.centralwidget)
        self.init_data_ui.resize(100,100)
        self.init_data_ui.move(Divide, 0)
        button =  QtWidgets.QLabel(self.init_data_ui)
        button.setText("我是数据分析窗口")
        lable = QtWidgets.QLabel(self.init_data_ui)
        lable.setText("看他")
        self.init_data_ui.hide()

    def init_log_view(self):
        self.init_log_ui = CViewLog(self.centralwidget, self)
        global_obj.set_obj("ViewLog", self.init_log_ui)

    def init_test_view(self):
        self.init_test_ui = CViewTest(self.centralwidget, self)

    def hide_all_ui(self):
        self.init_fund_ui.hide()
        self.init_data_ui.hide()
        #self.init_log_ui.hide()
        self.init_test_ui.hide()

    ################### 事件处理 ################
    #侧边目录被点击
    def on_menu_tree_click(self,indexobj):
        item = self.menu_tree.currentItem()
        text = item.text(0)
        self.hide_all_ui()
        if text == "基金爬虫":
            self.on_show_fund_spiker_ui()
        elif text == "数据分析":
            self.on_show_data_analyse()
        elif text == "测试":
            self.on_show_test()
    

    #菜单目录被点击
    def on_menu_triggered(self, action):
        print("object:",action.objectName())


    def on_show_fund_spiker_ui(self):
        self.init_fund_ui.show()
  
    def on_show_data_analyse(self):
        self.init_data_ui.show()


    def on_show_test(self):
        self.init_test_ui.show()
    

    def resizeEvent(self, event):
        self.menu_tree.OnResizeWindow(self)
        self.init_log_ui.OnResizeWindow(self)
        self.init_test_ui.OnResizeWindow(self)


