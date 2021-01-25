# -*- coding: utf-8 -*-
from defines import *
from PyQt5 import QtCore, QtGui, QtWidgets
from view import Ui_log_view

from .widget import CInterface

import math
import log

class CCacheLog(object):
    __cache_line = 2000
    __cache_cut = 100
    def __init__(self, filename = None):
        self.cache_list = []
        self.m_cache_str = None
        self.m_file_name = filename
        self.m_file = None
        if self.m_file_name: 
            self.m_file = open(filename, mode="a+")
    
    def fwrite(self, str):
        if not self.m_file:
            return
        self.m_file.write(str+"\n")



    def __del__(self):
        if self.m_file :
            self.m_file.close()

    def writeline(self, lineobj):
        text = lineobj.message_text()
        self.fwrite(text)
        color_text = str(lineobj)
        self.cache_list.append(color_text)
        if self.m_cache_str:
            self.m_cache_str += "<br>"+color_text
        if self.trim_cache() :
            return True

    
    def trim_cache(self):
        if len(self.cache_list) <= self.__cache_line:
            return False
        for _ in range(self.__cache_cut):
            self.cache_list.pop(0)
        self.m_cache_str = None
        return True
        
    def get_text(self):
        if self.m_cache_str is None:
            self.m_cache_str = "<br>".join( self.cache_list)

        return self.m_cache_str


class CViewLog(QtWidgets.QWidget, CInterface):
    def __init__(self, parent, MainWndow):
        super().__init__(parent)
        self.ui_obj = Ui_log_view()
        self.ui_obj.setupUi(self)
        self.ui_obj.textBrowser.resize(MainWindowWidth-Divide, MainWindowHeight - 50)
        self.cache_obj = CCacheLog()
        self.show()

    def OnResizeWindow(self, MainWindow):
        height = math.floor( MainWindow.height() * LogLow /100)
        y = MainWindow.height() - height
        self.move(0,y)
        self.resize(MainWindow.width(),height)
        self.ui_obj.textBrowser.resize(self.width(), self.height()-50)
       # self.ui_obj.line.resize(self.width(), 10)
    
    def println(self, lineobj):
        self.cache_obj.writeline(lineobj)
        self.ui_obj.textBrowser.setText(self.cache_obj.get_text())
        if self.ui_obj.checkBox.isChecked():
            self.ui_obj.textBrowser.moveCursor(self.ui_obj.textBrowser.textCursor().End)
