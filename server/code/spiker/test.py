# -*- coding: utf-8 -*-

import requests
import json
import re
from lxml import etree

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

    for ls in r:
        key = ls[0].replace(" ","")
        val = ls[1].replace(" ","")
        print(key)
    print("%dKB"%(len(text)/1024))
    #获取持仓股票信息
    #https://push2.eastmoney.com/api/qt/ulist.np/get?cb=jQuery18306482784578776678_1610895737356&fltt=2&invt=2&ut=267f9ad526dbe6b0262ab19316f5a25b&fields=f3,f12,f14&secids=0.002127,0.002013,1.601318,0.002271,0.300142,1.600519,0.000513,0.002475,0.000858,0.002444&_=1610895737461
    #基本信息
    #http://fund.eastmoney.com/000001.html

def fund_base():
    url = "http://fund.eastmoney.com/000001.html"
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
    top_stock_ratio = float(stock.xpath('.//p[@class="sum"]/span[@class="sum-num"]/text()')[0].replace("%",""))
    #持仓信息
    top_stock = {}
    stock_list = stock.xpath(".//tr")
    for v in stock_list:
        data = v.xpath("./td")
        if len(data) == 0 :
            continue
        name = data[0].xpath("./a/@title")[0]
        ratio = float(data[1].text.replace("%",""))
        top_stock[name] = ratio

    #债券信息
    bond = ls[1]
    top_bond_ratio  = float(bond.xpath('.//p[@class="sum"]/span[@class="sum-num"]/text()')[0].replace("%",""))
    
    bond_list = bond.xpath(".//tr")
    top_bond = {}
    for v in bond_list:
        data = v.xpath("./td")
        if len(data) == 0 :
            continue
        name = data[0].text
        ratio = float(data[1].text.replace("%",""))
        top_bond[name] = ratio
    result = {
        "top_stock":top_stock,
        "top_stock_ratio":top_stock_ratio,
        "top_bond":top_bond,
        "top_bond_ratio":top_bond_ratio,
    }
    return result


    

if __name__ == "__main__":
    print(fund_base())

