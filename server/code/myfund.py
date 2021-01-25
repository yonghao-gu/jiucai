# -*- coding: utf-8 -*-
import sys
import os

import global_obj
import log

from task import CTimeTrigger,CTask



def test1(taskobj, a):
    print("test1",taskobj,a)

def test2(taskobj, a):
    print("test2", taskobj,a)


def check_fund_status():
    config = global_obj.get_obj("config")
    fund_list = config.get("fund_list", [])
    if len(fund_list) == 0:
        log.Waring("fund_list is empty")
        return
    

def init_fund_task():
    task_timer = global_obj.get_obj("task_timer")

    time1 = CTimeTrigger(CTimeTrigger.TDay, "11:50:00")
    taskobj1 = CTask("check_fund", time1, check_fund_status, run_type = CTask.TForever)
    task_timer.AddTask(taskobj1)









