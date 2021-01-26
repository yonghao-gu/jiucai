# -*- coding: utf-8 -*-

import json


def load_config(file):
    f = open(file, "r")
    s = f.read()
    data = json.loads(s)
    f.close()
    return data


    



