# -*- coding: utf-8 -*-

from defines import *
from PyQt5 import QtCore, QtGui, QtWidgets
from view import Ui_log_view
from view import Ui_config_dialog
from .widget import CInterface

import globals

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
        conf_obj = globals.get_obj("Config").get_config()
        ui = self.ui_obj
        ui.addrEdit.setText(conf_obj.db_addr)
        ui.portEdit.setText(conf_obj.db_port)
        ui.accountEdit.setText(conf_obj.db_account)
        ui.passwordEdit.setText(conf_obj.db_password)
        

    def get_conf(self):
        data = {}
        ui = self.ui_obj
        data["db_addr"] = ui.addrEdit.text()
        data["db_port"] = ui.portEdit.text()
        data["db_account"] = ui.accountEdit.text()
        data["db_password"] = ui.passwordEdit.text()
        return data

    

    def OnSaveButtonClicked(self):
        conf_obj = globals.get_obj("Config")
        conf = self.get_conf()
        if not conf_obj.set_config(conf):
            QtWidgets.QMessageBox.warning(self, "参数错误", "输入参数有误")
            return
        QtWidgets.QMessageBox.information(self, "设置成功","成功！")
        self.close()

    def OnCancelButtonClicked(self):
        self.close()

    # def OnFinishDialg(self, r):
    #     pass