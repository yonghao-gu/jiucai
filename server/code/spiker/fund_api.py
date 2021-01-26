# -*- coding: utf-8 -*-
from defines import COLLECTION

from spiker_api import str2number, js2py_val, get_url
from lxml import etree


import requests
import json
import re
import time

import mongo_api
import global_obj

#获取基金基本信息
def fund_base(id):
    url = "http://fund.eastmoney.com/%s.html"%(str(id))
    result = get_url(url)
    assert result.status_code == 200, "网页获取失败:%s"%(url)
    tree = etree.HTML(result.text)

    ############  获取净值信息  #############
    net_worth = "0" #当前净值
    new_worth_ratio = "0"
    new_worth_sum = "0" #累计净值
    new_worth_update = "" #更新时间

    data2_tree = tree.xpath('//div[@class="fundDetail-main"]//dl[@class="dataItem02"]')[0]

    #更新日期
    ls = data2_tree.xpath("./dt/p/text()")
    if len(ls) == 1:
        s = ls[0].replace("(","")
        new_worth_update = ls[0].replace("(","").replace(")","")
    
    #单位净值
    ls = data2_tree.xpath('.//dd[@class="dataNums"]/span/text()')
    if len(ls) == 2:
        net_worth = ls[0]
        new_worth_ratio = ls[1].replace("%", "")

    #累计单位净值
    data3_tree = tree.xpath('//div[@class="fundDetail-main"]//dl[@class="dataItem03"]')[0]
    ls = data3_tree.xpath('.//dd[@class="dataNums"]/span/text()')
    if len(ls) > 0 and ls[0].find("%") == -1:
        new_worth_sum = ls[0]

    ############    解析基础信息    ##############
    ls = tree.xpath('//div[@class="infoOfFund"]//tr')
    fund_type = "暂无" #基金类型
    fund_scale = 0 #基金规模
    fund_manager = "无"

    if len(ls) > 0:
        info = ls[0]
        fund_type = info.xpath('./td[1]/a/text()')[0]
        text = info.xpath('./td[2]/text()')[0]
        r = re.match(r'.*?([\d|/.]+).*',text)
        if r :
            fund_scale = float(r.groups()[0])
        fund_manager = info.xpath('./td[3]/a/text()')[0]

    ############    解析仓位    ##############

    ls = tree.xpath('//div[@id="quotationItem_DataTable"]//div[@class="bd"]/ul/li')
    #股票信息
    #print(etree.tostring(stock_list[0], encoding="unicode", method = "html"))
    #前十占比
    top_stock_ratio = 0
    top_stock_date = ""
    #持仓信息
    top_stock = {}
    stock_list = []
    if  len(ls) > 0:
        stock = ls[0]
        stock_list = stock.xpath(".//tr")
    for v in stock_list:
        data = v.xpath("./td")
        if len(data) == 0 :
            continue
        if data[0].text.find("暂无数据") != -1 :
            break
        name = data[0].xpath("./a/@title")[0]
        ratio = float(data[1].text.replace("%",""))
        top_stock[name] = ratio
    if len(top_stock) > 0 :
        top_stock_ratio = float(stock.xpath('.//p[@class="sum"]/span[@class="sum-num"]/text()')[0].replace("%",""))
        date_time = stock.xpath('.//span[@class="end_date"]/text()')[0]
        r = re.match(".*? (.*)",date_time)
        top_stock_date = r.groups()[0]

    #债券信息
    bond_list = []
    top_bond = {}
    top_bond_ratio = 0
    top_bond_date = ""
    if len(ls) > 1:
        bond = ls[1]
        bond_list = bond.xpath(".//tr")
    for v in bond_list:
        data = v.xpath("./td")
        if len(data) == 0 :
            continue
        name = data[0].text
        if name.find("暂无数据") != -1:
            break
        ratio = float(data[1].text.replace("%",""))
        top_bond[name] = ratio
    
    if len(top_bond) > 0:
        top_bond_ratio  = float(bond.xpath('.//p[@class="sum"]/span[@class="sum-num"]/text()')[0].replace("%",""))
        date_time = bond.xpath('.//span[@class="end_date"]/text()')[0]
        r = re.match(".*? (.*)",date_time)
        top_bond_date = r.groups()[0]


    result = {
        "type":fund_type, #类型
        "scale":fund_scale, #规模
        "manager":fund_manager, #基金经理
        "stock":top_stock, #股票仓位
        "stock_ratio":top_stock_ratio, #股票占比
        "stock_date":top_stock_date, #股票更新日期
        "bond":top_bond, #债券
        "bond_ratio":top_bond_ratio, #债券占比
        "bond_date":top_bond_date, #债券日期
        "net_worth":net_worth, #当前净值
        "new_worth_ratio":new_worth_ratio, #涨跌
        "new_worth_sum":new_worth_sum, #累计净值
        "new_worth_update":new_worth_update, #更新日期
    }
    return result


def _compress_networth(ls):
    result_ls = []
    for d in ls:
        result_ls.append([d["x"],d["y"], d.get("equityReturn", "0"), d.get("unitMoney", "")])
    return result_ls


def _compress_Scale(data):
    if not "categories" in data:
        return []
    categories = data["categories"]
    series = data["series"]
    result = []
    for i in range(len(categories)):
        d = series[i]
        result.append([categories[i], d["y"], d["mom"]])
    return result

def _compress_assetAllocation(data):
    result = {}
    result["categories"] = data.get("categories", [])
    series = {}
    for d in data.get("series", []):
        series[d["name"]] = d["data"]
    result["series"] = series
    return result


def _compress_manager(data):
    result = []
    for cur_manager in data:
        info = {
            "id" :  cur_manager.get("id",""),
            "name": cur_manager.get("name", "无"),
            "workTime": cur_manager.get("workTime",""),
            "fundSize":cur_manager.get("fundSize", "0")
        }
        result.append(info)
    return result



#获取基金公司具体信息
def fund_data(code):
    url = "http://fund.eastmoney.com/pingzhongdata/%s.js"%code
    result = get_url(url)
    if result.status_code != 200 :
        return
    text = result.text
    #获取所有值
    r = re.findall(r"var(.*?)=(.*?);",text)
    env = {}
    for ls in r:
        key = ls[0].replace(" ","")
        val = ls[1].replace(" ","")
        val = js2py_val(val)
        env[key] = val
    assert env["fS_code"] == code, "code is different"
    Data_grandTotal = env.get("Data_grandTotal", [])
    if len(Data_grandTotal) > 0:
        Data_grandTotal = Data_grandTotal[0].get("data", [])
    result = {
        "code" : env["fS_code"], #基金代码\
        "yield": { #收益率 近3年,近1年，今年来,近6个月，
            "month6":str2number(env["syl_6y"]),
            "year1":str2number(env["syl_1n"]),
            "month3":str2number(env["syl_3y"]),
            "month1":str2number(env["syl_1y"]),
        },
        "name": env["fS_name"], #名字
        "total":{ #具体数据
            "scale":_compress_Scale(env.get("Data_fluctuationScale",{})), #基金规模
            "net_worth":_compress_networth(env.get("Data_netWorthTrend",[])), #净值走势
            "newworth_total":Data_grandTotal, #累计净值
            "asset_allocation":_compress_assetAllocation(env.get("Data_assetAllocation", {})), #资产规模
        },
        "manger":_compress_manager(env.get("Data_currentFundManager", [])),
    }
    return result


#爬取基金所有信息
def spiker_fund(code):
    base = fund_base(code)
    t = fund_data(code)
    data = {
        "code": code,
        "base" : base,
        "data" : t,
        "name" : t["name"]

    }
    return data

def spiker_fund_and_save(code):
    data = spiker_fund(code)
    save_fund(code, data)
    return data


################################# 数据库对象 ########################

def save_fund(code, data):
    dbobj = global_obj.get_obj("dbobj")
    col = dbobj.Collection(COLLECTION["fund"][0])
    col.update({"code":code}, data, upsert = True )

def load_fund(code):
    dbobj = global_obj.get_obj("dbobj")
    col = dbobj.Collection(COLLECTION["fund"][0])
    ret = col.find_one({"code": code}, {"_id":0})
    return ret






def test_code():
    codelist = ["270002", "217011", "003474"]
    for code in codelist:
        print(fund_base(code))

