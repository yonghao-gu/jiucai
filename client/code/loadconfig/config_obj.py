# -*- coding: utf-8 -*-


class CConfig(object):
    __default_config = {
        "db_addr":"127.0.0.1",
        "db_port":"27107",
        "db_account":"root",
        "db_password":"pass",
    }

    def __init__(self, conf):
        self.m_conf = conf
    
    def get(self, key, defualt):
        return self.m_conf
    
    def set_conf(self, conf):
        self.m_conf = conf
    
    def set(self, key, val):
        self.m_conf[key] = val

