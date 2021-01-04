# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtWidgets, QtGui,QtCore

from override.oui_main import Oui_MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)

    mainwindow = Oui_MainWindow()
    #mainW.setWindowIcon(QIcon("./resource/icon.jpg"))
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()