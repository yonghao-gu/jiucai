# -*- coding: utf-8 -*-

import json


def load_config(file):
    f = open(file, "r")
    s = f.read()
    data = json.loads(s)
    f.close()
    return data

class CConfig(object):
    def __init__(self, conf):
        self.m_conf = conf
    
    def __getattribute__(self, attr):
        if attr in self.m_conf:
            return self.m_conf.get(attr, None)
    



