# -*- coding: utf-8 -*-
from defines import *
from PyQt5 import QtCore, QtGui, QtWidgets
from view import Ui_log_view

from .widget import CInterface

import math

class CViewLog(QtWidgets.QWidget, CInterface):
    def __init__(self, parent, MainWndow):
        super().__init__(parent)
        self.ui_obj = Ui_log_view()
        self.ui_obj.setupUi(self)
        self.ui_obj.textBrowser.resize(MainWindowWidth-Divide, MainWindowHeight - 50)
        self.show()

    def OnResizeWindow(self, MainWindow):
        height = math.floor( MainWindow.height() * LogLow /100)
        y = MainWindow.height() - height
        self.move(0,y)
        self.resize(MainWindow.width(),height)
        self.ui_obj.textBrowser.resize(self.width(), self.height())
        self.ui_obj.line.resize(self.width(), 10)
    
    def println(self, text):
        self.ui_obj.textBrowser.append(text)