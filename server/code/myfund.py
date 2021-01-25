# -*- coding: utf-8 -*-
import sys
import os


from task import CTimeTrigger,CTask

import global_obj
import log
import spiker.fund_api as fund_api
import html
import mail_box


def check_fund_status(taskobj):
    config = global_obj.get_obj("config")
    fund_list = config.get("fund_list", [])
    if len(fund_list) == 0:
        log.Waring("fund_list is empty")
        return
    ls = []
    for code in fund_list:
        old = fund_api.load_fund(code)
        code = str(code)
        fund_api.spiker_fund_and_save(code)
        ret = fund_api.load_fund(code)
        log.Info("spiker fund done", code)
        if old and ret:
            result = compare_fund(old,ret)
            if result:
                ls.append(result)
        else:
            log.Waring("load fund false", taskobj, type(old), type(ret))

    log.Info("spiker fund all", len(ls))
    if len(ls) > 0:
        htmobj = html.CHtml("你的韭菜日报:")
        for v in ls:
            line = "基金：%s(%s) 变化"%(v["name"],v["code"])
            htmobj.AddLine(line)
            htmobj.AddDict2Table(v["data"])
        html_text = htmobj.GetHtml()
        mailobj = global_obj.get_obj("mail")
        message  = mailobj.HtmlMailMessage()
        if message.SendMessage("韭菜研报", html_text):
            log.Info("send jiucai mail done")




def key_copy(tbl, keys):
    data = {}
    for key in keys:
        if key in tbl:
            data[key] = tbl[key]
    return data

def compare_fund(old,new):
    base_old = old["base"]
    base_new = new["base"]
    force = True
    keys_list = ["fund_manager"]
    if force or base_old["stock_date"] != base_new["stock_date"]:
        keys_list.extend(["stock", "stock_ratio", "stock_date"])
    if force or base_old["bond_date"] != base_new["bond_date"]:
        keys_list.extend(["bond", "bond_ratio", "bond_date"])
    if force or base_old["scale"] != base_new["scale"]:
        keys_list.extend(["scale"])
    if len(keys_list) == 1:
        return
    ls = []
    ls.extend([key_copy(base_old, keys_list), key_copy(base_new, keys_list)])
    result = {
        "data":ls,
        "code":new["code"],
        "name":new["name"]
    }
    return result


def init_fund_task():
    task_timer = global_obj.get_obj("task_timer")
    #time1 = CTimeTrigger(CTimeTrigger.TDay, "11:50:00")
    time1 = CTimeTrigger(CTimeTrigger.TCycle, 10)
    taskobj1 = CTask("check_fund", time1, check_fund_status, run_type = CTask.TForever)
    task_timer.AddTask(taskobj1)









