# -*- coding: utf-8 -*-

import requests
import json
import re
from lxml import etree




#获取页面基本信息
def fund_base(id):
    url = "http://fund.eastmoney.com/%s.html"%(str(id))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    }
    result = requests.get(url = url, headers = headers)
    assert result.status_code == 200, "网页获取失败:%s"%(url)
    result.encoding ="utf-8"
    tree = etree.HTML(result.text)
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