# -*- coding: utf-8 -*-

import global_obj



class CFileLog(object):
    def __init__(self, file = None):
        self.m_file = file
        self.m_fp = None
        self.try_open()
    
    def try_open(self):
        if not self.m_file:
            return
        if self.m_fp :
            return
        try:
            self.m_fp = open(self.m_file, "a+")
        except IOError as error:
            print("file open false", error)
    
    def write(self, s):
        self.try_open()
        if not self.m_fp:
            return
        try:
            self.m_fp.write(s)
            self.m_fp.flush()
        except IOError as error:
            print("write file false", error)
            if self.m_fp:
                self.m_fp.close()
                self.m_fp = None
    
    def println(self, obj):
        text = obj.message_text()
        print(text)
        self.write(text+"\n")
        

def init_logger():
    config = global_obj.get_obj("config")
    file = None
    if  "log" in config:
        file = config["log"]
    logger = CFileLog(file)
    global_obj.set_obj("logger", logger)
