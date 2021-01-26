# -*- coding: utf-8 -*-

from defines import *
from PyQt5 import QtCore, QtGui, QtWidgets
from view import Ui_log_view
from view import Ui_config_dialog
from .widget import CInterface

import global_obj

class CConfigDialg(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui_obj = Ui_config_dialog()
        self.ui_obj.setupUi(self)

        #self.finished.connect(self.OnFinishDialg)


        self.set_label()
        self.ui_obj.SaveButton.clicked.connect(self.OnSaveButtonClicked)
        self.ui_obj.CancelButton.clicked.connect(self.OnCancelButtonClicked)

    def SetLineEdit(self):
        self.ui_obj.portEdit.setValidator(QtGui.QIntValidator())
        reg = QtCore.QRegExp('[A-Za-z0-9_\-\u4e00-\u9fa5]+')
        validator = QtGui.QRegExpValidator()
        validator.setRegExp(reg)
        self.ui_obj.addrEdit.setValidator(validator)
        self.ui_obj.accountEdit.setValidator(validator)
        self.ui_obj.passwordEdit.setValidator(validator)

    def set_label(self):
        db_conf = global_obj.get_obj("Config")["db"]
        ui = self.ui_obj
        ui.addrEdit.setText(db_conf["addr"])
        ui.portEdit.setText(db_conf["port"])
        ui.accountEdit.setText(db_conf["user"])
        ui.passwordEdit.setText(db_conf["password"])
        

    def get_conf(self):
        data = {}
        ui = self.ui_obj
        data["db_addr"] = ui.addrEdit.text()
        data["db_port"] = ui.portEdit.text()
        data["db_account"] = ui.accountEdit.text()
        data["db_password"] = ui.passwordEdit.text()
        return data

    

    def OnSaveButtonClicked(self):
        # conf_obj = global_obj.get_obj("Config")
        # conf = self.get_conf()
        # if not conf_obj.set_config(conf):
        #     QtWidgets.QMessageBox.warning(self, "参数错误", "输入参数有误")
        #     return
        # QtWidgets.QMessageBox.information(self, "设置成功","成功！")
        self.close()

    def OnCancelButtonClicked(self):
        self.close()

    # def OnFinishDialg(self, r):
    #     pass