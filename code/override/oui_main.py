# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

#from view import Ui_MainWindow
from view import Ui_fund_view



class Oui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("韭菜收割机")
        self.resize(600,700)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralframe")
        self.setCentralWidget(self.centralwidget)
        self.setWindowIcon(QtGui.QIcon("resource/main_icon.jpg"))


        self.memu_tree = QtWidgets.QTreeWidget(self.centralwidget)
        self.memu_tree.setGeometry(QtCore.QRect(0, 10, 131, 541))
        self.memu_tree.setObjectName("memu_tree")
        self.memu_tree.setColumnCount(1)
        self.memu_tree.setHeaderLabels(["目录"])

        child1 = QtWidgets.QTreeWidgetItem(self.memu_tree)
        child1.setText(0, "爬虫")

        child1_1 = QtWidgets.QTreeWidgetItem(child1)
        child1_1.setText(0, "基金爬虫")

        child1_2 = QtWidgets.QTreeWidgetItem(child1)
        child1_2.setText(0, "股票采集")


        child2 = QtWidgets.QTreeWidgetItem(self.memu_tree)
        child2.setText(0,"数据分析")

        child3 = QtWidgets.QTreeWidgetItem(self.memu_tree)
        child3.setText(0, "日志")

        self.init_fund_spiker_ui()
        self.init_data_analyse()
        self.memu_tree.clicked.connect(self.on_memu_tree_click)
        
    def init_fund_spiker_ui(self):
        self.init_fund_ui = QtWidgets.QWidget(self.centralwidget)
        self.init_fund_ui.resize(300,600)
        self.init_fund_ui.move(150,200)
        button = QtWidgets.QPushButton()
        button.setText("我是爬虫窗口")
        lable = QtWidgets.QLabel()
        lable.setText("看他")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(lable)
        self.init_fund_ui.setLayout(layout)
        self.init_fund_ui.hide()
        self.init_log_view()


    def init_data_analyse(self):
        self.init_data_ui = QtWidgets.QWidget(self.centralwidget)
        self.init_data_ui.resize(300,600)
        self.init_data_ui.move(150,200)
        button =  QtWidgets.QLabel()
        button.setText("我是数据分析窗口")
        lable = QtWidgets.QLabel()
        lable.setText("看他")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(lable)
        self.init_data_ui.setLayout(layout)
        self.init_data_ui.hide()

    def init_log_view(self):
        self.init_log_ui = QtWidgets.QWidget(self.centralwidget)
        obj = Ui_fund_view()
        obj.setupUi(self.init_log_ui)
        #self.init_log_ui.resize(300, 400)
        self.init_log_ui.move(150,160)
        # lable = QtWidgets.QLabel()
        # lable.setText("日志")
        # layout = QtWidgets.QHBoxLayout()
        # layout.addWidget(lable)
        #obj.setupUi(layout)
        #self.init_log_ui.setLayout(layout)
        self.init_log_ui.show()

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



