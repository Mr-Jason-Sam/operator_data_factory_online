# -*- coding: UTF-8 -*-
"""
@Description : 香港交易所数据
@Author      : Jason_Sam
@Time        : 2021/4/13 10:57

"""
import json

import requests_tools
import time_tools
from official_config import HKexConfig

"""
:@deprecated: 获取北向资金数据
:@param: 爬虫地址
:@return: 返回净买入额和交易总额
"""


def __fetch_north_money(url):
    # 获取url数据
    net_data = requests_tools.fetch_net_data(url)
    text = net_data.text
    # 解析页面数据
    js = text[text.index('{'):(text.rindex('}') + 1)]
    js = json.loads(js)
    buy = js['section'][0]['item'][1][1]
    sell = js['section'][0]['item'][2][1]
    buy_mil = ''.join(list(filter(str.isdigit, buy)))
    sell_mil = ''.join(list(filter(str.isdigit, sell)))
    # net_buy_mil = float(buy_mil) - float(sell_mil)
    # sh_total = float(buy_mil) + float(sell_mil)
    return float(buy_mil), float(sell_mil)


"""
:@deprecated: 获取沪港通数据
:@param: 时间
:@return: 
"""
def fetch_hk_to_sh(date_time: str = None):
    if date_time is None:
        # 获取当前毫秒级时间戳
        date_time = str(time_tools.get_now_timestamp(time_tools.TimeUnit.millisecond))
    return __fetch_north_money(HKexConfig.hk_to_sh_url + date_time)

"""
:@deprecated: 获取深港通数据
:@param: 时间
:@return: 
"""
def fetch_hk_to_sz(date_time: str = None):
    if date_time is None:
        # 获取当前毫秒级时间戳
        date_time = str(time_tools.get_now_timestamp(time_tools.TimeUnit.millisecond))
    return __fetch_north_money(HKexConfig.hk_to_sz_url + date_time)
