# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget,QMainWindow,QPushButton,QLabel,QVBoxLayout,QDialog,QApplication,QTableWidget,QItemDelegate, \
                            QTableWidgetItem
from PyQt5.QtGui import QPainter,QIcon
from PyQt5.QtCore import Qt,QSize,pyqtSignal




class CMyWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.resize(300,400)
    
    def paintEvent(self, event):
        pen = QPainter()
        pen.begin(self)
        pen.setPen(Qt.blue)
        pen.drawRect(0,0,100,100)
        pen.drawLine(0,0,100,100)
        pen.end()

class CMyButton(QPushButton):
    signal_1 = pyqtSignal()
    signal_2 = pyqtSignal(int)
    signal_3 = pyqtSignal([int,str],[list])
    signal_4 = pyqtSignal([int],[str])

    def run_signal(self):
        self.signal_1.emit()
        self.signal_2.emit(123)
        self.signal_3[int,str].emit(134,"hello")
        self.signal_3[list].emit([111,222,333])
        self.signal_4[int].emit(999)
        self.signal_4[str].emit("ppppppp")


class CMyMainWindow(QMainWindow):
    def __init__(self, parent = None):
       # super(CMyMainWindow,self).__init__(parent)
        super().__init__(parent)
        self.setWindowTitle("第一个程序")
        self.resize(600,600)
        mainframe = QWidget(self)
        mainframe.setObjectName("centralframe")

        self.setCentralWidget(mainframe)

        self.tablew = QTableWidget(3,4)
        # self.tablew.setColumnCount(4)
        # self.tablew.setRowCount(4)
        self.tablew.setHorizontalHeaderLabels(["姓名","年龄","班级","分数"])
        self.tablew.setVisible(True)
        self.tablew.setItemDelegate(QItemDelegate(self))
        box = QVBoxLayout(mainframe)
        ls = [
            ["泥泞", "39","3A","45"],
            ["安妮", "44","3B", "20"],
            ["李磊","20","4A", "23"],
        ]
        for row,l in enumerate(ls):
            for col, v in enumerate(l):
                item = QTableWidgetItem(v)
                item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
                self.tablew.setItem(row,col, item)
                self.tablew.setBaseSize(QSize(500,100))
 
        box.addWidget(self.tablew)
        button = CMyButton("点我", mainframe)
        button.clicked.connect(self.on_click)
        button.signal_1.connect(self.on_signal_1)
        button.signal_2.connect(self.on_signal_1)
        button.signal_3[int,str].connect(self.on_signal_1)
        button.signal_3[list].connect(self.on_signal_1)
        button.signal_4[int].connect(self.on_signal_1)
        button.signal_4[str].connect(self.on_signal_1)
        box.addWidget(button)
        
        self.setLayout(box)


    def on_click(self):
        button = self.sender()
        button.run_signal()
    
    def on_signal_1(self, *args):
        print("on_signal_1",args)
    
    def on_signal_2(self,a):
        print("on_signal_2",a)

    def OnClickClose(self):
        print("new dialog")
        wdg = QDialog()
        button = QPushButton("确认", wdg)
        #button.clicked.connect(wdg.close)
        button.move(50,50)
        wdg.setWindowTitle("对话框")
        wdg.setWindowModality(Qt.ApplicationModal)
        wdg.exec()


def main():
    app = QApplication(sys.argv)
    mainW = CMyMainWindow()
    mainW.setWindowIcon(QIcon("./resource/icon.jpg"))
    mainW.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    
    main()
