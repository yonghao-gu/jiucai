# -*- coding: utf-8 -*-
from defines import *
from PyQt5 import QtCore, QtGui, QtWidgets
from view import Ui_log_view

from .widget import CInterface


class CViewLog(QtWidgets.QWidget, CInterface):
    def __init__(self, parent, MainWndow):
        super().__init__(parent)
        self.ui_obj = Ui_log_view()
        self.ui_obj.setupUi(self)
        self.ui_obj.textBrowser.resize(MainWindowWidth-Divide, MainWindowHeight - 50)
        self.move(Divide,0)
        self.hide()
        

    def OnResizeWindow(self, MainWindow):
        self.resize(MainWindow.width()-Divide,MainWindow.height())
        self.ui_obj.textBrowser.resize(self.width(), self.height())
 