# -*- coding: utf-8 -*-

from spiker_api import str2number, js2py_val, get_url

from lxml import etree

import requests
import json
import re
import time




#获取基金基本信息
def fund_base(id):
    url = "http://fund.eastmoney.com/%s.html"%(str(id))
    result = get_url(url)
    assert result.status_code == 200, "网页获取失败:%s"%(url)
    tree = etree.HTML(result.text)
    ############    解析基础信息    ##############
    ls = tree.xpath('//div[@class="infoOfFund"]//tr')
    fund_type = "暂无" #基金类型
    fund_scale = "0" #基金规模
    if len(ls) > 0:
        info = ls[0]
        fund_type = info.xpath('./td[1]/a/text()')[0]
        text = info.xpath('./td[2]/text()')[0]
        print(type(text),text)
        r = re.match(r".*?([\d}\.]*?)\D.*",text)
        print(r.groups())
        fund_manager = info.xpath('./td[3]/a/text()')[0]
        print(fund_type, text, fund_manager)

    ############    解析仓位    ##############

    ls = tree.xpath('//div[@id="quotationItem_DataTable"]//div[@class="bd"]/ul/li')
    #股票信息
    stock = ls[0]
    #print(etree.tostring(stock_list[0], encoding="unicode", method = "html"))
    #前十占比
    top_stock_ratio = 0
    top_stock_date = ""
    #持仓信息
    top_stock = {}
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
    bond = ls[1]
    bond_list = bond.xpath(".//tr")
    top_bond = {}
    top_bond_ratio = 0
    top_bond_date = ""
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
        "stock":top_stock,
        "stock_ratio":top_stock_ratio,
        "stock_date":top_stock_date,
        "bond":top_bond,
        "bond_ratio":top_bond_ratio,
        "bond_date":top_bond_date,
    }
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
            "scale":env["Data_fluctuationScale"], #基金规模
        },
    }
    return result


