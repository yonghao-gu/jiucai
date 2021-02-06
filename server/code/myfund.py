# -*- coding: utf-8 -*-
import sys
import os


from task import CTimeTrigger,CTask
from spiker.key2word import fund_word

import global_obj
import log
import spiker.fund_api as fund_api
import thread_api
import html
import mail_box
import tools


def tofloat(s):
    return tools.tofloat(s, 4)

@tools.check_use_time(0.5, tools.global_log, "关注基金用时")
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
    else:
        log.Info("基金信息没有变化")


def set_color(new_val,old_val):
    if not tools.is_float(new_val) or not tools.is_float(old_val):
        return new_val
    nf = tofloat(new_val)
    of = tofloat(old_val)

    if nf > of:
        return html.html_font(str(new_val), "red")
    elif nf == of:
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
        keys_list.extend(["new_worth", "new_worth_ratio", "new_worth_sum", "new_worth_update"])
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
    ls = combine_dict(base_new, base_old, keys_list, hook_func)
    head = ["变量","旧值","新值"]
    result = {
        "data":ls,
        "head": head,
        "code":new["code"],
        "name":new["name"]
    }
    return result

__filter_stop_type = set([
    "混合型","股票指数","股票型"
])

@tools.check_use_time(0, tools.global_log, "线程爬虫用时")
def thread_spike_fund(threadobj, *fund_list):
    ok = 0
    err = 0
    i=0
    l = len(fund_list)
    fund_yeild = {}
    stock_total = {}
    for code in fund_list:
        i+=1
        if i%50 == 0:
            log.Info("thread_spike_fund",threadobj.getName(),i,l-i)
        try:
            data = fund_api.spiker_fund_and_save(code)
            base_data = data["base"]
            if not base_data["type"] in __filter_stop_type:
                continue
            if not tools.is_float(base_data["new_worth_ratio"]):
                continue
            for k,v in base_data["stock"].items():
                if not k in stock_total:
                    stock_total[k] = 0
                stock_total[k]+=1
            fund_yeild[code] = {
                "now": base_data["new_worth_ratio"],
                "history":data["data"]["yield"],
                "name": data["name"]
            }
            ok+=1
        except BaseException as error:
            log.Error("spiker fund false", threadobj.getName(), code, error)
            err+=1
            continue

    return {
        "ok":ok,
        "error":err,
        "data":{
            "stock":stock_total,
            "yeild":fund_yeild,
        },
    }


def split_args(count,fund_list):
    args_list = []
    l = len(fund_list)
    n = int(l/count) + 1
    start,end = 0,n
    for i in range(count):
        ll = fund_list[start:end]
        start,end = end,end+n
        if len(ll) == 0:
            break
        args_list.append(ll)
    return args_list

@tools.check_use_time(0, tools.global_log, "爬取所有基金用時")
def update_all_fund(taskobj):
    fund_list = fund_api.fund_all()
    l = len(fund_list)
    log.Info("update_all_fund", taskobj, l)
    thread_num = 5
    args_list = split_args(thread_num,fund_list)
    result = thread_api.start_args(thread_spike_fund, args_list)
    all_ok = 0
    all_error = 0
    stock_total = {}
    top_fund = []
    for data in result:
        all_ok+=data["ok"]
        all_error+=data["error"]
        tools.combine_dict(stock_total, data["data"]["stock"])
        for code, v in data["data"]["yeild"].items():
            top_fund.append((code, v))
    
    top_stock = [ (k, v) for k,v in stock_total.items() ]
    top_stock = sorted(top_stock, key = lambda k:tofloat(k[1]), reverse = True)
    top_fund = sorted(top_fund, key = lambda d:tofloat(d[1]["now"]), reverse = True)

    with open("stock_list.txt", "w") as fp:
        for v in top_stock:
            fp.write("%s    %s\n"%(v[0],v[1]))

    top20stock = top_stock[:40]
    top20fund = top_fund[:20]
    tail20fund = list(reversed(top_fund[len(top_fund) - 20:]))

    def make_fund(fund_list):
        ls = []
        for v in fund_list:
            code = v[0]
            data = v[1]
            d = data["history"]
            l = [data["name"], code, data["now"], 
                d.get("month1",0), d.get("month3", 0), d.get("month6", 0) ,d.get("year1", 0)
                ]
            ls.append(l)
        return ls


    htmobj = html.CHtml("韭菜排行:")
    if len(top20stock) > 0:
        htmobj.AddLine("基金持仓top20股票")
        htmobj.AddTable(top20stock, head = ["股票名","基金持有数"])

    head = ["基金名","代码","今日收益", "近1月收益", "近3月收益", "近6月收益", "近1年收益"]
    if len(top20fund) > 0:
        htmobj.AddLine("收益top20")
        htmobj.AddTable(make_fund(top20fund), head = head)
    if len(tail20fund) > 0:
        htmobj.AddLine("亏损top20")
        htmobj.AddTable(make_fund(tail20fund), head = head)

    html_text = htmobj.GetHtml()
    mailobj = global_obj.get_obj("mail")
    message  = mailobj.HtmlMailMessage()
    if message.SendMessage("韭菜排行榜", html_text):
        log.Info("send jiucai mail done")

    

def init_fund_task():
    task_timer = global_obj.get_obj("task_timer")
    time1 = CTimeTrigger(CTimeTrigger.TDay, "23:40:00")
    taskobj1 = CTask("check_fund", time1, check_fund_status, run_type = CTask.TForever)
    task_timer.AddTask(taskobj1)

    time2 = CTimeTrigger(CTimeTrigger.TDay, "23:50:00")
    taskobj2 = CTask("update_all", time2, update_all_fund, run_type = CTask.TForever)
    task_timer.AddTask(taskobj2)



def test_code():
    update_all_fund("no task")
    # code_list = ["000485", "000486", "000369"]
    # for code in code_list:
    #     print(fund_api.fund_base(code))






