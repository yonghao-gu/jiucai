# -*- coding: utf-8 -*-
import sys
import os
import time

#2000年的1月3号周一作为开始时间
_start_time = int(time.mktime((2000,1,3,0,0,0,0,0,0)))

def start_time():
    return _start_time

def second():
    return int(time.time())

def get_day_no(ti):
    return int((ti - _start_time)/86400)

def get_week_no(ti):
    return int((ti - _start_time) / 604800)

def is_same_day(t1,t2):
    return get_day_no(t1) == get_day_no(t2)

def is_same_week(t1, t2):
    return get_week_no(t1) == get_week_no(t2)


def get_week_day(ti):
    return time.localtime(ti).tm_wday + 1

#获取0点时间
def get_today_start(ti):
    return _start_time + get_day_no(ti) * 86400





