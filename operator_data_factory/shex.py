# -*- coding: UTF-8 -*-
"""
@Description : 上海交易所数据
@Author      : Jason_Sam
@Time        : 2021/4/13 10:57

"""
import json

import requests_tools
import time_tools
from official_config import SHexConfig

"""
:@deprecated: 获取上交所代码的点位和涨跌幅
:@param: 
:@return: 返回 (名称、点位、涨跌幅)
"""
def fetch_quote_info(code: str, date_time: str = None):
    if date_time is None:
        # 获取当前毫秒级时间戳
        date_time = str(time_tools.get_now_timestamp(time_tools.TimeUnit.millisecond))
    url = SHexConfig.quote_url_prefix + code + SHexConfig.quote_url_suffix + date_time
    net_data = requests_tools.fetch_net_data(url)
    text = net_data.text
    js = text[text.index('{'):(text.rindex('}') + 1)]
    js = json.loads(js)
    # print(js['snap'][0] + ':' + str(js['snap'][1]) + ', 涨跌幅:' + str(js['snap'][2]) + '%')
    return js['snap'][0], js['snap'][1], js['snap'][2], js['snap'][3]
