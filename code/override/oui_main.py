# -*- coding: utf-8 -*-

from defines import *

from PyQt5 import QtCore, QtGui, QtWidgets
#from view import Ui_MainWindow
from view import Ui_fund_view
from view import Ui_log_view

from components import CViewMemu, CViewLog

import globals

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


        self.memu_tree = CViewMemu(self.centralwidget,self)


        self.init_fund_spiker_ui()
        self.init_data_analyse()
        self.init_log_view()
        self.memu_tree.clicked.connect(self.on_memu_tree_click)
    

        
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
        # layout = QtWidgets.QHBoxLayout()
        # layout.addWidget(button)
        # layout.addWidget(lable)
        # self.init_data_ui.setLayout(layout)
        self.init_data_ui.hide()

    def init_log_view(self):
        self.init_log_ui = CViewLog(self.centralwidget, self)
        globals.set_obj("ViewLog", self.init_log_ui)



    def hide_all_ui(self):
        self.init_fund_ui.hide()
        self.init_data_ui.hide()
        self.init_log_ui.hide()

    def on_memu_tree_click(self,indexobj):
        item = self.memu_tree.currentItem()
        text = item.text(0)
        self.hide_all_ui()
        if text == "基金爬虫":
            self.on_show_fund_spiker_ui()
        elif text == "数据分析":
            self.on_show_data_analyse()
        elif text == "日志":
            self.on_show_log()
    
    def on_show_fund_spiker_ui(self):
        self.init_fund_ui.show()
  
    def on_show_data_analyse(self):
        self.init_data_ui.show()

    def on_show_log(self):
        self.init_log_ui.show()


    def resizeEvent(self, event):
        self.memu_tree.OnResizeWindow(self)
        self.init_log_ui.OnResizeWindow(self)



