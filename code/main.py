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

    mainwindow = Oui_MainWindow()
    globals.set_obj("MainWindow", mainwindow)
    #mainW.setWindowIcon(QIcon("./resource/icon.jpg"))
    mainwindow.show()
    log.Sys("启动成功")
    # logobj = globals.get_obj("ViewLog")
    # print(logobj.ui_obj.textBrowser.toPlainText())
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()