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


