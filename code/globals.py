# -*- coding: utf-8 -*-

g_objs = {}

def set_obj(name, obj):
    global g_objs
    assert(not name in g_objs)
    g_objs[name] = obj

def get_obj(name):
    return g_objs[name]




