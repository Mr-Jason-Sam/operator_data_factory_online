# -*- coding: UTF-8 -*-
"""
@Description : 深圳交易所数据
@Author      : Jason_Sam
@Time        : 2021/4/13 10:58

"""
import json

import requests_tools
from official_config import SZexConfig

"""
:@deprecated: 获取深交所代码的点位和涨跌幅
:@param: 
:@return: 返回 (名称、点位、涨跌幅)
"""
def fetch_latest_quote_info(code: str):
    url = SZexConfig.quote_url + code
    net_data = requests_tools.fetch_net_data(url)
    text = net_data.text
    js = json.loads(text)
    # print(js['data']['name'] + ':' + js['data']['now'] + ', 涨跌幅:' + str(js['data']['deltaPercent']) + '%')
    return js['data']['name'], float(js['data']['now']), float(js['data']['deltaPercent']), float(js['data']['amount'])
