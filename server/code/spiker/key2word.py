# -*- coding: utf-8 -*-
'''
将变量名转换为中文
'''

WORDS = {
    "type" : "基金类型",
    "scale": "规模（亿）",
    "manager": "基金经理",
    "stock":"股票持仓",
    "stock_date": "股票更新日期",
    "stock_ratio": "股票占比",
    "bond":"债券",
    "bond_ratio":"债券占比",
    "bond_date":"债券更新日期",
    "name": "基金",
    "code":"代码",
    "net_worth":"当前净值",
    "new_worth_ratio":"涨跌",
    "new_worth_sum":"累计净值",
    "new_worth_update":"净值更新",
}


def fund_word(name):
    return WORDS.get(name, name)

'''
{'混合型': 382, '债券型': 186, '定开债券': 80,
 '联接基金': 22, '货币型': 191, '股票指数': 23, 'QDII': 17, 
'QDII-指数': 11, '股票型': 83, '理财型': 3, '债券指数': 2}
'''

FUND_TYPE = {
  1:"混合型",
  2:"债券型",
  3:"定开债券",
  4:"联接基金",
  5:"货币型",
  6:"股票指数",
  7:"QDII",
  8:"II-指数",
  9:"股票型",
  10:"理财型",
  11:"债券指数"

}

FUND_DESC2TYPE = {

}

def __fund_desc2type():
    global FUND_DESC2TYPE,FUND_TYPE
    for k,v in FUND_TYPE.items():
        FUND_DESC2TYPE[v] = k










