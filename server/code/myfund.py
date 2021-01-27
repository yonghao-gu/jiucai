# -*- coding: utf-8 -*-
import sys
import os


from task import CTimeTrigger,CTask
from spiker.key2word import fund_word

import global_obj
import log
import spiker.fund_api as fund_api
import html
import mail_box
import tools

@tools.check_use_time(0.5, tools.global_log)
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
            htmobj.AddTable(v["data"], v["head"])
        html_text = htmobj.GetHtml()
        mailobj = global_obj.get_obj("mail")
        message  = mailobj.HtmlMailMessage()
        if message.SendMessage("韭菜研报", html_text):
            log.Info("send jiucai mail done")


def set_color(new_val,old_val):
    if not tools.is_float(new_val) or not tools.is_float(old_val):
        return new_val

    if float(new_val) > float(old_val):
        return html.html_font(str(new_val), "red")
    elif float(new_val) == float(old_val):
        return new_val
    else:
        return html.html_font(str(new_val), "green")

def __hook_top(tbl, key, default):
    if not key in tbl:
        return default
    text = ""
    for name,r in tbl[key].items():
        text+= html.html_br("%s:%s"%(name,r))
    return text


def combine_dict(new, old, keys, hookfuns = None):
    ls = []
    for key in keys:
        if hookfuns and key in hookfuns:
            n = hookfuns[key](new, key, "")
            o = hookfuns[key](old, key, "")
        else:
            n = new.get(key, "")
            o = old.get(key, "")
        n = set_color(n, o)
        ls.append([fund_word(key), o, n])
    return ls


def compare_fund(old, new):
    base_old = old["base"]
    base_new = new["base"]
    force = False
    keys_list = ["manager"]
    if force or base_old["new_worth_update"] != base_new["new_worth_update"]:
        keys_list.extend(["net_worth", "new_worth_ratio", "new_worth_sum", "new_worth_update"])
    if force or base_old["stock_date"] != base_new["stock_date"]:
        keys_list.extend(["stock", "stock_ratio", "stock_date"])
    if force or base_old["bond_date"] != base_new["bond_date"]:
        keys_list.extend(["bond", "bond_ratio", "bond_date"])
    if force or base_old["scale"] != base_new["scale"]:
        keys_list.extend(["scale"])
    if len(keys_list) == 1:
        return
    hook_func = {
        "stock":__hook_top,
        "bond": __hook_top,
    }
    ls = combine_dict(base_new, base_new, keys_list, hook_func)
    head = ["变量","旧值","新值"]
    result = {
        "data":ls,
        "head": head,
        "code":new["code"],
        "name":new["name"]
    }
    return result





def init_fund_task():
    task_timer = global_obj.get_obj("task_timer")
    time1 = CTimeTrigger(CTimeTrigger.TDay, "23:50:00")
    #time1 = CTimeTrigger(CTimeTrigger.TCycle, 10)
    taskobj1 = CTask("check_fund", time1, check_fund_status, run_type = CTask.TForever)
    task_timer.AddTask(taskobj1)









