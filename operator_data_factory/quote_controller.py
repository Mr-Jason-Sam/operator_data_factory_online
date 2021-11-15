# -*- coding: UTF-8 -*-
"""
@Description : 行情控制器
@Author      : Jason_Sam
@Time        : 2021/4/13 15:25

"""
import sys

import business_config
import business_tools
from base_quote import BaseQuote
from cache import BusinessCache
from close_mkt_info import CloseMktInfo
from daily_review_service import DailyReviewService
from ifund_quote import IFundQuote
from index_base_info import IndexBaseInfo


class QuoteController:

    def __init__(self):
        self.__daily_review_service = DailyReviewService()

    """
    :@deprecated: 获取指数数据
    :@param: 
    :@return: 
    """

    def get_index_base_quote(self):
        key = sys._getframe().f_code.co_name
        is_trade_time = business_tools.is_trade()

        # 非交易时间可使用缓存数据
        if not is_trade_time:
            quote_data = BusinessCache().get_cache().get(key)
            if quote_data is not None:
                return quote_data

        quote_data = self.__daily_review_service.fetch_base_index_quote()

        if not is_trade_time:
            BusinessCache().get_cache().set(key, quote_data)

        return quote_data

    """
    :@deprecated: 获取行业领涨领跌幅
    :@param: 
    :@return: 
    """

    def get_industry_top_bottom(self):
        key = sys._getframe().f_code.co_name
        is_trade_time = business_tools.is_trade()

        # 非交易时间可使用缓存数据
        if not is_trade_time:
            quote_demo = BusinessCache().get_cache().get(key)
            if quote_demo is not None:
                return quote_demo

        # 获取申万二级涨跌板块
        ifund_quote = IFundQuote()
        data = ifund_quote.fetch_daily_top_bottom_change_on_sw_second(business_config.SW_SECOND_INDUSTRY_IFUND)

        top_industry_df = data[0][[IndexBaseInfo.name, BaseQuote.latest_price, BaseQuote.change_ratio]]
        bottom_industry_df = data[1][[IndexBaseInfo.name, BaseQuote.latest_price, BaseQuote.change_ratio]]

        industry_data = {
            CloseMktInfo.top_industry: top_industry_df,
            CloseMktInfo.bottom_industry: bottom_industry_df
        }

        if not is_trade_time:
            BusinessCache().get_cache().set(key, industry_data)

        return industry_data

    """
       :@deprecated: 获取所有行业行情数据
       :@param: 
       :@return: 
       """

    def get_industry(self):
        # 获取申万二级涨跌板块
        ifund_quote = IFundQuote()
        return ifund_quote.fetch_industry_info(business_config.SW_SECOND_INDUSTRY_IFUND)
