# -*- coding: utf-8 -*-

import globals
import time

DEF_LEVEL = {
    "Log":      "#C0C0C0", #灰
    "Info":     "#000000", #黑
    "Debug":    "#00FF00", #绿
    "Waring":   "#FF8040", #橙
    "Error":    "#FF0000", #红
    "Sys":      "#0000FF", #蓝
    "Failure":  "#8A2BE2", #紫
}

def add_message(level, str):
    t = time.localtime()
    now = time.strftime("%Y-%m-%d %H:%M:%S",t)
    return "[%s %s]"%(now, level) + str

def color(level, str):
    return '''<font size="5" color="%s">%s</fornt>'''%(DEF_LEVEL[level], str)


def log_obj():
    return globals.get_obj("logger")

def write_log(level, *args):
    ls = [ str(i) for i in args]
    s = " ".join(ls)
    obj = ClineObj(s, level)
    log_obj().println(obj)

class ClineObj(object):
    def __init__(self, s, level):
        self.m_text = s
        self.m_level = level
    
    def color_text(self, s = None):
        return color(self.m_level, s or self.m_text)
    
    def messae_text(self, s = None):
        return add_message(self.m_level, s or self.m_text)
    
    def text(self):
        return self.color_text(self.messae_text())
    
    def origin(self):
        return self.m_text

    def __str__(self):
        return self.text()
    
class CFileLogger(object):
    def __init__(self, file):
        pass


def Log(*args):
    write_log("Log", *args)

def Info(*args):
    write_log("Info", *args)

def Debug(*args):
    write_log("Debug", *args)

def Waring(*args):
    write_log("Waring", *args)


def Error(*args):
    write_log("Error", *args)

def Sys(*args):
    write_log("Sys", *args)

def Failure(*args):
    write_log("Failure", *args)

