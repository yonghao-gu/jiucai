# -*- coding: utf-8 -*-
import sys
import os
import time

# libpath = os.path.abspath("./lib")
# sys.path.append(libpath)

import global_obj

import time_api
import log

class CTaskTimer(object):
    __sleep = 5

    def __init__(self, abort = None):
        self.m_task = []
        self.m_abort = abort
    
    def AddTask(self, taskobj):
        log.Sys("AddTask", taskobj)
        self.m_task.append(taskobj)
    
    def RunForever(self):
        while(True):
            time.sleep(CTaskTimer.__sleep)
            self.RunTask()
            if self.__CheckAbort():
                break
        log.Sys("TaskTimer is stop")
    
    def RunTask(self):
        rm_task = []
        for taskobj in self.m_task:
            if not taskobj.CanRun():
                continue
            taskobj.Run()
            if taskobj.IsOver():
                print("task over", str(taskobj))
                rm_task.append(taskobj)

        for taskobj in rm_task:
            self.m_task.remove(taskobj)
        
    def __CheckAbort(self):
        print("check stop", self.m_abort)
        if not self.m_abort :
            return False
        if os.path.exists(self.m_abort):
            os.remove(self.m_abort)
            return True
        return False
        

class CTimeTrigger(object):
    '''
CTimTrigger 定义何时被触发
支持触发类型
1 周期触发： ti(second)表示触发的间隔 ti = 60 表示每60秒触发一次
2 每日触发:  ti(str) 表示每天触发的时间 ti = "23:30:00" 表示23点30分触发
3 每周触发:  ti(str)表示每周触发的时间 ti = "1-23:30:00" 表示周一23:30分触发

设置误差类型：
    1. 运行当前时间大于触发时间15秒的间隔
    2. 当前时间时间>触发时间即可

'''

    TCycle = 1
    TDay = 2
    TWeek = 3

    def __init__(self, trigger_type, ti):
        self.m_trigger_type = trigger_type
        self.m_now = time_api.start_time()  #设置为最早的一天
        self.__check_args(ti)
    
    def __check_args(self, ti):
        if self.m_trigger_type == CTimeTrigger.TCycle:
            assert type(ti) == int, "args false"
            self.m_args = (ti,)
        elif self.m_trigger_type == CTimeTrigger.TDay:
            ls = ti.split(":")
            assert len(ls) == 3, "args false"
            ti = ls[0]*3600 + ls[1]*60 + ls[2]
            self.m_args = (ti,)
        elif self.m_trigger_type == CTimeTrigger.TWeek:
            ls = ti.split("-")
            day = ls[0]
            ti = ls[1]
            ls = ti.split(":")
            ti = ls[0]*3600 + ls[1]*60 + ls[2]
            self.m_args = (day, ti)
        else:
            raise "trigger_type false"
    
    def __recyle_can_triger(self):
        return time_api.second() - self.m_now > self.m_args[0]

    def __today_can_trigger(self):
        now = time_api.second()
        if time_api.is_same_day(now, self.m_now):
            return False
        return  now >= (time_api.get_today_start(now) + self.m_args[0])

    def __week_can_trigger(self):
        now = time_api.second()
        if time_api.is_same_week(now, self.m_now):
            return False
        if time_api.get_week_day(now) != self.m_args[0]:
            return False
        return now >= (time_api.get_today_start(now) + self.m_args[1])

    def CanTrigger(self):
        if self.m_trigger_type == CTimeTrigger.TCycle:
            return self.__recyle_can_triger()
        elif self.m_trigger_type == CTimeTrigger.TDay:
            return self.__today_can_trigger()
        else:
            return self.__week_can_trigger()
    
        
    
    def Trigger(self):
        self.m_now = time_api.second()
        



class CTask(object):
    __id = 0
    __None = 0
    __Running = 1
    __Over = 2
    
    TOnce = 1 #只执行一次
    TForever = 2 #永远执行
    def __new_id(self):
        CTask.__id += 1
        return CTask.__id

    def __init__(self, name, timeTigger, func, **kwg):
        self.m_status = CTask.__None
        self.m_name = name
        self.m_id = self.__new_id()
        self.m_trigger = timeTigger
        self.m_type = CTask.TOnce
        self.m_func = func
        self.m_args = ()
        self.__check__(kwg)
    
    def __check__(self, kwg):
        if "args" in kwg:
            assert type(kwg["args"]) == tuple, "args must be tuple"
            self.m_args = kwg["args"]
        if "run_type" in kwg:
            assert kwg["run_type"] == CTask.TOnce or kwg["run_type"] == CTask.TForever, "run_type false"
            self.m_type = kwg["run_type"]
    
    def __str__(self):
        return "<%s:%d>"%(self.m_name, self.m_id)
    
    def IsRunning(self):
        return self.m_status == CTask.__Running

    def IsRunOnce(self):
        return self.m_type == CTask.TOnce
    
    def IsRunForver(self):
        return self.m_type == CTask.TForever

    def IsOver(self):
        return self.m_status == CTask.__Over

    def CanRun(self):
        if self.IsRunning():
            return False
        if not self.m_trigger.CanTrigger():
            return False
        return True

    def Run(self):
        try:
            self.m_trigger.Trigger()
            self.m_func(self, *self.m_args)
        except BaseException as error:
            self.m_status = CTask.__Over
            print("run task fail",str(self),error)
        else:
            if self.IsRunOnce():
                self.m_status = CTask.__Over
            elif self.IsRunForver():
                self.m_status = CTask.__None
    





def init_task():
    config = global_obj.get_obj("config")
    abortfile = None
    if "abort" in config:
        abortfile = config["abort"]
    timetaskobj = CTaskTimer(abortfile)
    global_obj.set_obj("task_timer", timetaskobj)

if __name__ == "__main__":
    init_task()

