# -*- coding: UTF-8 -*-
"""
@Description : 时间工具类
@Author      : Jason_Sam
@Time        : 2021/4/13 13:36

"""
import time
from datetime import datetime


class TimeUnit:
    # 秒
    seconds = 's'
    # 毫秒
    millisecond = 'ms'
    # 微秒
    microsecond = 'us'


class TimeFormat:
    yyyy_mm_dd_hh_ms = '%Y-%m-%d%H:%M'
    yyyy_mm_dd = '%Y%m%d'


weekday = ['星期一',
           '星期二',
           '星期三',
           '星期四',
           '星期五',
           '星期六',
           '星期日']

"""
:@deprecated: 获取当前时间戳
:@param: 
:@return: 
"""


def get_now_timestamp(unit: TimeUnit):
    if TimeUnit.seconds == unit:
        return int(time.time())
    elif TimeUnit.millisecond == unit:
        return int(round(time.time() * (10 ** 3)))
    elif TimeUnit.microsecond == unit:
        return int(round(time.time() * (10 ** 6)))
    else:
        return int(time.time())


"""
:@deprecated: 判断当天时间是否在范围内
:@param: 
:@return: 
"""


def is_between(begin_time, end_time, now=None):
    begin_time = datetime.strptime(str(datetime.now().date()) + begin_time, TimeFormat.yyyy_mm_dd_hh_ms)
    end_time = datetime.strptime(str(datetime.now().date()) + end_time, TimeFormat.yyyy_mm_dd_hh_ms)

    if begin_time > end_time:
        raise Exception('起始时间不可大于结束时间')

    if now is None:
        # 当前时间
        now = datetime.now()

    # 判断当前时间是否在范围时间内
    if begin_time <= now <= end_time:
        return True
    else:
        return False


"""
:@deprecated: 获取日期的星期
:@param: 
:@return: 
"""


def get_week_day_zh(now=None):
    if now is None:
        now = datetime.now()
    day_of_week = now.weekday()

    return weekday[day_of_week]


"""
:@deprecated: 获取日期的月日
:@param: 
:@return: 
"""
def get_mm_dd_zh(now=None):
    if now is None:
        now = datetime.now()

    return now.strftime("%m{m}%d{d}").format(m="月", d="日")


