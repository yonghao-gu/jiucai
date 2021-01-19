# -*- coding: utf-8 -*-

import requests
import json
import re
from lxml import etree

import fund_api
import demjson
import time
import json
import ast


def main():
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    }
    result = requests.get(url = url, headers = headers)
    if result.status_code != 200 :
        print("result false")
        return
    text = result.text
    #content = result.content.encode("utf-8")
    #print(result.content)

    #x = text[text.find("var r = "):]
    r = re.match("var r = (.*)",text)
    js_code = r.groups()[0]
    # js_data = json.loads(js_text)
    global_data={"data":None}
    code = '''
global data
data = %s
'''%(js_code)
    result = exec(code, global_data)
    print("data:",type(global_data["data"]))

#literal_eval 不能处理非js对象的值，但demjson效率太慢，所以采用异常机制让denjson处理非js对象
def js2py_val(val):
    try:
        val = ast.literal_eval(val) 
    except BaseException as error:
        val = demjson.decode(val)
    return val

def main2():
    #获取基金公司信息
    url = "http://fund.eastmoney.com/pingzhongdata/000001.js"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    }
    result = requests.get(url = url, headers = headers)
    if result.status_code != 200 :
        print("result false")
        return
    text = result.text
    #获取所有值
    r = re.findall(r"var(.*?)=(.*?);",text)
    env = {}
    t1 = time.time()
    for ls in r:
        key = ls[0].replace(" ","")
        val = ls[1].replace(" ","")
        val = js2py_val(val)
        env[key] = val
    print("len:%d - men:%dKB"%(len(env),len(text)/1024))

    print("use time:", time.time() - t1)
    #获取持仓股票信息
    #基本信息
    #http://fund.eastmoney.com/000001.html





def fund_base():
    url = "http://fund.eastmoney.com/217011.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    }
    result = requests.get(url = url, headers = headers)

    if result.status_code != 200 :
        print("result false")
        return
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


    

if __name__ == "__main__":
    main2()

