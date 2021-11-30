# -*- coding: UTF-8 -*-
"""
@Description : 同花顺接口
@Author      : Jason_Sam
@Time        : 2021/4/9 13:16

"""
from time import sleep

from iFinDPy import THS_iFinDLogin, THS_iFinDLogout

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

    """
    :@deprecated: 登出
    :@param: 
    :@return: 
    """

    def logout(self):
        sleep(5)
        return THS_iFinDLogout()
