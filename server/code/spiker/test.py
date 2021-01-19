# -*- coding: utf-8 -*-

import os
import sys

libpath = os.path.abspath("./lib")
sys.path.append(libpath)


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




if __name__ == "__main__":
    test = False
    ls = ["000001", "006482","213917", "002937","010270"]
    f = fund_api.fund_data
    f = fund_api.fund_base
    if test :
        for i in ls:
            print(f(i))
    else:
        print(f("000001"))

