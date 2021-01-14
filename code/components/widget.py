# -*- coding: utf-8 -*-
from defines import *
from PyQt5 import QtCore, QtGui, QtWidgets

import math


class CInterface(object):
    def OnResizeWindow(self, MainWindow):
        pass

class CCoreInterface(CInterface):
    def OnResizeWindow(self, MainWindow):
        y = math.floor( MainWindow.height() * LogLow /100)
        height = math.floor(MainWindow.height() * (100 - LogLow) / 100)
        self.move(Divide+1,0)
        self.resize(MainWindow.width() - Divide,height)

