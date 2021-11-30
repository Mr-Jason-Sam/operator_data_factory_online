# -*- coding: UTF-8 -*-
"""
@Description : 行情数据
@Author      : Jason_Sam
@Time        : 2021/4/9 14:24

"""
import json
import logging
import sys

import pandas as pd
from iFinDPy import *

import business_tools
from base_quote import BaseQuote
from cache import BusinessCache
from ifund_client import IFundClient
from index_base_info import IndexBaseInfo


class IFundQuote:

    def __init__(self):
        self.__ifund_client = IFundClient()
        self.__cache = BusinessCache().get_cache()

    """
    :@deprecated: 获取指数的基础数据（目前暂时获取名称）
    :@param: 
    :@return: 
    """

    def fetch_index_base_info(self, index_list_str: str):
        index_base_info_key = sys._getframe().f_code.co_name + index_list_str
        index_df = self.__cache.get(index_base_info_key)

        if index_df is not None:
            return index_df

        # 获取同花顺数据
        self.__ifund_client.login()
        index = THS_BasicData(index_list_str, 'ths_index_short_name_index', '', True)

        logging.info('index info: ' + str(index))

        # 处理同花顺数据，转化为df
        index_js = json.loads(index.decode('gbk'))
        index_df = pd.DataFrame(data=index_js['tables'])
        index_df[IndexBaseInfo.name] = index_df['table'].map(lambda x: x['ths_index_short_name_index'][0])
        index_df.rename(columns={'thscode': IndexBaseInfo.code}, inplace=True)
        index_df = index_df[[IndexBaseInfo.code, IndexBaseInfo.name]]

        # 登出
        self.__ifund_client.logout()

        self.__cache.set(index_base_info_key, index_df)

        return index_df

    """
    :@deprecated: 获取指数的基础行情信息（最新价和涨跌幅）
    :@param: 
    :@return: 
    """

    def fetch_index_base_quote(self, index_list_str: str):

        quote_base_info_key = sys._getframe().f_code.co_name + index_list_str
        quote_df = self.__cache.get(quote_base_info_key)

        is_trade_time = business_tools.is_trade()

        # 非交易时间可使用缓存数据
        if quote_df is not None and not is_trade_time:
            return quote_df

        # 获取同花顺数据
        self.__ifund_client.login()
        quote = THS_RealtimeQuotes(index_list_str, 'tradeDate;latest;changeRatio', '', True)

        logging.info('quote info: ' + str(quote))

        # 处理同花顺数据，转化为df
        quote_js = json.loads(quote.decode('gbk'))
        quote_df = pd.DataFrame(data=quote_js['tables'])
        quote_df[BaseQuote.trade_date] = quote_df['table'].map(lambda x: str(x['tradeDate'][0]).replace('-', ''))
        quote_df[BaseQuote.latest_price] = quote_df['table'].map(lambda x: round(x['latest'][0], 2) if x['latest'][0] is not None else None)
        quote_df[BaseQuote.change_ratio] = quote_df['table'].map(lambda x: round(x['changeRatio'][0], 2) if x['changeRatio'][0] is not None else None)
        quote_df.dropna(inplace=True)
        quote_df.rename(columns={'thscode': BaseQuote.code}, inplace=True)
        quote_df = quote_df[[BaseQuote.trade_date, BaseQuote.code, BaseQuote.latest_price, BaseQuote.change_ratio]]

        # 登出
        self.__ifund_client.logout()

        if not is_trade_time:
            self.__cache.set(quote_base_info_key, quote_df)

        return quote_df

    """
    :@deprecated: 获取领涨领跌的N个申万二级板块
    :@param: 
    :@return: 
    """

    def fetch_daily_top_bottom_change_on_sw_second(self, index_list_str: str, num: float = 3):
        assemble_df = self.fetch_industry_info(index_list_str=index_list_str)

        top_index_df = assemble_df.sort_values(by=BaseQuote.change_ratio, ascending=False).iloc[:num].reset_index(drop=True)
        bottom_index_df = assemble_df.sort_values(by=BaseQuote.change_ratio, ascending=True).iloc[:num].reset_index(drop=True)

        return top_index_df, bottom_index_df

    """
    :@deprecated: 获取所有的申万二级板块数据
    :@param: 
    :@return: 
    """
    def fetch_industry_info(self, index_list_str):
        industry_info_key = sys._getframe().f_code.co_name + index_list_str
        quote_df = self.__cache.get(industry_info_key)

        is_trade_time = business_tools.is_trade()

        # 非交易时间可使用缓存数据
        if quote_df is not None and not is_trade_time:
            return quote_df
        index_info_df = self.fetch_index_base_info(index_list_str=index_list_str)
        index_quote_df = self.fetch_index_base_quote(index_list_str=index_list_str)

        assemble_df = pd.merge(left=index_info_df,
                               right=index_quote_df,
                               how='outer',
                               on=[IndexBaseInfo.code]).dropna()

        assemble_df = assemble_df.sort_values(by=BaseQuote.change_ratio, ascending=False)

        self.__cache.set(industry_info_key, assemble_df)

        return assemble_df
