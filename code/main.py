# -*- coding: utf-8 -*-
import sys



from PyQt5 import QtWidgets, QtGui,QtCore
from override.oui_main import Oui_MainWindow
from view import Ui_fund_view

import globals
import log
import time

def main():
    app = QtWidgets.QApplication(sys.argv)
    globals.set_obj("App", app)
    mainwindow = Oui_MainWindow()
    globals.set_obj("MainWindow", mainwindow)
    #mainW.setWindowIcon(QIcon("./resource/icon.jpg"))
    mainwindow.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()