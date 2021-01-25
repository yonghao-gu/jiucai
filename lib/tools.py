# -*- coding: utf-8 -*-
import time
import log

def __default_log(*args):
    print("已用时",args)

def check_use_time(time_limit, log):
    if not log:
        log = print
    def default_decorator(func):
        def wrappend_func(*args, **kwargs):
            fs = time.time()
            ret = func(*args, **kwargs) 
            if time.time() - fs > time_limit:
                log("流程总用时：%d"%(time.time() - fs))
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