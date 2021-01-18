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

def main3():
    url = "http://fund.eastmoney.com/000001.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    }
    result = requests.get(url = url, headers = headers)

    if result.status_code != 200 :
        print("result false")
        return
    result.encoding ="utf-8"
    text = result.text
    tree = etree.HTML(text)
    ls = tree.xpath('//div[@class="bd"]')[2].xpath("./ul//tr")[1:]

    for v in ls:
        l = v.xpath("./td")
        print(len(l))
    print(ls)

if __name__ == "__main__":
    main3()

