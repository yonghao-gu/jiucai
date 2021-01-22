# -*- coding: utf-8 -*-

def __default_log(*args):
    print("maio:",args)

def check_use_time(time_limit, log):
    if not log:
        log = print
    def default_decorator(func):
        def wrappend_func(*args, **kwargs):
            fs = time.time()
            ret = func(*args, **kwargs) 
            log("流程总用时：%d"%(time.time() - fs))
            return ret
        return wrappend_func
    return default_decorator



