# -*- coding: UTF-8 -*-
"""
@Description : 业务工具类
@Author      : Jason_Sam
@Time        : 2021/4/14 17:42

"""
import business_config
import time_tools

"""
:@deprecated: 当前是否为A股的交易时间（未处理交易日历和特殊情况，例如熔断，休市半天等）
:@param: 
:@return: 
"""
def is_trade(now_time=None):
    return time_tools.is_between(begin_time=business_config.A_MARKET_OPEN_TIME_AM,
                                 end_time=business_config.A_MARKET_CLOSE_TIME_AM,
                                 now=now_time) or \
           time_tools.is_between(begin_time=business_config.A_MARKET_OPEN_TIME_PM,
                                 end_time=business_config.A_MARKET_CLOSE_TIME_PM,
                                 now=now_time)

