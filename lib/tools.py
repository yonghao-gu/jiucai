# -*- coding: utf-8 -*-
import time
import log

def __default_log(*args):
    print("已用时",args)

def check_use_time(time_limit, log, desc = "流程总用时:"):
    if not log:
        log = print
    def default_decorator(func):
        def wrappend_func(*args, **kwargs):
            fs = time.time()
            ret = func(*args, **kwargs) 
            if time.time() - fs > time_limit:
                log("%s %d"%(desc, time.time() - fs))
            return ret
        return wrappend_func
    return default_decorator


def global_log(*args):
    log.Sys(*args)

def is_float(s):
    try:
        float(s)
    except BaseException as e:
        return False
    return True

def tofloat(s, point = 2):
    if not is_float(s) :
        return 0.0
    fmt = "%%.%df"%(point)
    return float(fmt%(float(s)))



def combine_dict(dict1, dict2):
    for k,v in dict2.items():
        if k in dict1 and type(dict1[k]) == int and type(v) == int:
            dict1[k]+=v
        else:
            if not k in dict1:
                dict1[k] = v


