# -*- coding: utf-8 -*-

import requests
import json
import re
import jiphy
import js2py

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
    url = "http://fund.eastmoney.com/pingzhongdata/000001.js"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    }
    result = requests.get(url = url, headers = headers)
    if result.status_code != 200 :
        print("result false")
        return
    text = result.text
    # r = re.findall(r"var(.*?)=(.*?);",text)
    # for ls in r:
    #     key = ls[0].replace(" ","")
    #     val = ls[1].replace(" ","")
    #     print(key)
    print("%dKB"%(len(text)/1024))



if __name__ == "__main__":
    main2()

