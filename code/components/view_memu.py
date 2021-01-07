# -*- coding: utf-8 -*-
from defines import *
from PyQt5 import QtCore, QtGui, QtWidgets

from .widget import CInterface


class CViewMemu(QtWidgets.QTreeWidget, CInterface):
    def __init__(self, parent, MainWndow):
        super().__init__(parent)
        self.setObjectName("memu_tree")
        self.setColumnCount(1)
        self.OnResizeWindow(MainWndow)
        self.setHeaderLabels(["目录"])
        child1 = QtWidgets.QTreeWidgetItem(self)
        child1.setText(0, "爬虫")

        child1_1 = QtWidgets.QTreeWidgetItem(child1)
        child1_1.setText(0, "基金爬虫")

        child1_2 = QtWidgets.QTreeWidgetItem(child1)
        child1_2.setText(0, "股票采集")


        child2 = QtWidgets.QTreeWidgetItem(self)
        child2.setText(0,"数据分析")

        child3 = QtWidgets.QTreeWidgetItem(self)
        child3.setText(0, "日志")





    def OnResizeWindow(self, MainWindow):
        self.setGeometry(QtCore.QRect(0, 0, Divide, MainWindow.height()))












