# -*- coding: utf-8 -*-
from defines import *
from PyQt5 import QtCore, QtGui, QtWidgets

from .widget import CCoreInterface

from view import Ui_Test

import log


class CViewTest(QtWidgets.QWidget, CCoreInterface):
    def __init__(self, parent, MainWndow):
        super().__init__(parent)
        self.ui_obj = Ui_Test()
        self.ui_obj.setupUi(self)
        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QtGui.QColor(192,253,123))
        self.setPalette(palette1)
        self.hide()
        self.ui_obj.pushButton.clicked.connect(self.OnPushButton)
    
    def OnPushButton(self, isclicked):
        s = self.ui_obj.lineEdit.text()
        log.Sys(s)
    


