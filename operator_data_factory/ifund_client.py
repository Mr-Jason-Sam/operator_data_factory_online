# -*- coding: UTF-8 -*-
"""
@Description : 同花顺接口
@Author      : Jason_Sam
@Time        : 2021/4/9 13:16

"""
from iFinDPy import THS_iFinDLogin

from ifund_config import IFundConfig


class IFundClient:

    def __init__(self):
        self.__user = IFundConfig.user
        self.__password = IFundConfig.password

    """
    :@deprecated: 登录
    :@param: 
    :@return: 
    """

    def login(self):
        THS_iFinDLogin(self.__user, self.__password)



