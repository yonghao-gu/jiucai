# -*- coding: utf-8 -*-
import sys

import json
import time
def __log(*args):
    print("maio:",args)

def paramter(log = None):
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

@paramter()
def main(a,b):
    print("hello",a,b)

if __name__ == "__main__":
    
    main(33,444)
