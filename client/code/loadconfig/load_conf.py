# -*- coding: utf-8 -*-
from view import Ui_config_dialog
from components import CConfigDialg
import common
from PyQt5 import QtCore, QtGui, QtWidgets

import log

class CConfig(object):
    default_config = {
        "db_addr":"127.0.0.1",
        "db_port":"27107",
        "db_account":"root",
        "db_password":"pass",
    }

    def __init__(self, conf):
        self.m_conf = conf
    
    def get(self, key):
        return self.m_conf.get(key, CConfig.default_config[key])
    
    def __getattribute__(self, attr):
        if attr in CConfig.default_config:
            return self.m_conf.get(attr, CConfig.default_config[attr])
        return super().__getattribute__(attr)
    


class CLoadConfig(object):
    def __init__(self):
        self.m_conf = {}
    
    def get_config(self):
        return CConfig(self.m_conf)

    def set_config(self,conf):
        if not self.check_config(conf):
            log.Debug("配置错误")
            return False
        
        self.m_conf = conf
        return True
    
    def check_config(self,conf):
        obj = CConfig(conf)
        for k in CConfig.default_config.keys():
            func = getattr(self, "_check_"+k , None)
            if func and not func(obj.get(k)):
                return False
        
        return True


    def _check_db_addr(self, val):
        return common.isIP(val)

    def show_dialog(self):
        dialog = CConfigDialg()
        #dialog.finished.connect(self.OnFinishDialog)
        dialog.exec_()

