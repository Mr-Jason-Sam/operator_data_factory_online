# -*- coding: UTF-8 -*-
"""
@Description : 网络工具
@Author      : Jason_Sam
@Time        : 2021/4/13 13:48

"""
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

max_retries = 5

"""
:@deprecated: 获取网络数据
:@param: 
:@return: 
"""
def fetch_net_data(url: str):
    retries = Retry(total=max_retries,
                    backoff_factor=1,
                    status_forcelist=[500, 502, 503, 504])
    # Get方式获取网页数据
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=retries))  # 设置重试次数为10次
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s.get(url)
