# -*- coding: utf-8 -*-

import requests
import demjson
import ast


def str2number(val):
    if len(val) == 0 :
        return 0
    return float(val)


def js2py_val(val):
    try:
        val = ast.literal_eval(val) 
    except BaseException as error:
        val = demjson.decode(val)
    return val


def get_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    }
    result = requests.get(url = url, headers = headers)
    result.encoding ="utf-8"
    return result

def get_session_url(url, session = None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    }
    if not session:
        session = requests.session()
    
    result = session.get(url = url, headers = headers)
    result.encoding ="utf-8"
    return result, session
