# -*- coding: utf-8 -*-
import sys

import json

def main():
    data = {
        "db":{
            "addr" : "47.107.152.146",
            "port" : "8883",
            "user" : "jiucai",
            "password": "a82993344",
        }

    }
    print(json.dumps(data))

if __name__ == "__main__":
    
    main()
