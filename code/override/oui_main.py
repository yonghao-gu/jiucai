# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

# from view import Ui_MainWindow
# from view import Ui_Form
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
        self.memu_tree.clicked.connect(self.on_memu_tree_click)
        self.m_x = 140
        self.m_y = 50

    def on_memu_tree_click(self,indexobj):
        item = self.memu_tree.currentItem()
        if item.text(0) == "基金爬虫":
            self.init_fund_spiker_ui()
    
    def init_fund_spiker_ui(self):
        
        obj = QtWidgets.QWidget(self.centralwidget)
        obj.resize(300,600)
        obj.move(self.m_x,self.m_y)
        self.m_y += 100
        
        button = QtWidgets.QPushButton()
        button.setText("看我")
        lable = QtWidgets.QLabel()
        lable.setText("看他")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(lable)
        obj.setLayout(layout)
        obj.show()


