# -*- coding: UTF-8 -*-
"""
@Description : 业务缓存
@Author      : Jason_Sam
@Time        : 2021/4/9 14:44

"""
import threading

from cacheout import Cache

class BusinessCache:
    _instance_lock = threading.Lock()
    __business_cache = Cache()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(BusinessCache, "_instance"):
            with BusinessCache._instance_lock:
                if not hasattr(BusinessCache, "_instance"):
                    BusinessCache._instance = object.__new__(cls)
        return BusinessCache._instance

    def get_cache(self):
        return self.__business_cache
