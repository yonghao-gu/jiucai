# -*- coding: utf-8 -*-


import threading

class CThread(threading.Thread):

    def set_func(self, func, args):
        self.m_func = func
        self.m_args = args
        self.m_result = None

    def run(self):
        if not self.m_func:
            return
        self.m_result = self.m_func(self, *self.m_args)
    
    def result(self):
        return self.m_result

def start_args(func, thread_args):
    thread_list = []
    result_list = []
    i=0
    for args in thread_args:
        i+=1
        obj = CThread()
        obj.setName("thread_%d"%i)
        obj.set_func(func, args)

        thread_list.append(obj)
        obj.start()
    for obj in thread_list:
        obj.join()
        result_list.append(obj.result())
    return result_list

