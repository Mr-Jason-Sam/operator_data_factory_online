# -*- coding: UTF-8 -*-
"""
@Description : 行情数据
@Author      : Jason_Sam
@Time        : 2021/4/9 14:24

"""

import datetime as dt

import pandas as pd
from iFinDPy import *

import business_config
import business_tools
import date_constants
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
        quote_df = self.__cache.get(index_base_info_key)

        if quote_df is not None:
            return quote_df

        # 获取同花顺数据
        self.__ifund_client.login()
        quote = THS_BD(index_list_str, 'ths_index_short_name_index', '')

        quote_df = quote.data
        # 登出
        self.__ifund_client.logout()

        if quote_df is None or quote_df.empty:
            raise Exception(index_list_str + '数据为空！')

        # 处理同花顺数据，转化为df
        quote_df.rename(columns={'thscode': IndexBaseInfo.code,
                                 'ths_index_short_name_index': IndexBaseInfo.name}, inplace=True)

        self.__cache.set(index_base_info_key, quote_df)

        return quote_df

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
        quote = THS_RQ(index_list_str, 'tradeDate;latest;changeRatio', '')

        quote_df = quote.data
        # 登出
        self.__ifund_client.logout()

        if quote_df is None or quote_df.empty:
            raise Exception(index_list_str + '数据为空！')

        quote_df.rename(
            columns={
                'tradeDate': BaseQuote.trade_date,
                'thscode': BaseQuote.code,
                'latest': BaseQuote.latest_price,
                'changeRatio': BaseQuote.change_ratio},
            inplace=True
        )

        quote_df[BaseQuote.trade_date] = quote_df[BaseQuote.trade_date].map(lambda x: str(x).replace('-', ''))

        if not is_trade_time:
            self.__cache.set(quote_base_info_key, quote_df, ttl=date_constants.HALF_HOUR_SECONDS)

        return quote_df

    """
    :@deprecated: 获取领涨领跌的N个申万二级板块
    :@param: 
    :@return: 
    """

    def fetch_daily_top_bottom_change_on_sw_second(self, index_list_str: str, num: float = 3):
        assemble_df = self.fetch_industry_info(index_list_str=index_list_str)

        top_quote_df = assemble_df.sort_values(by=BaseQuote.change_ratio, ascending=False).iloc[:num].reset_index(
            drop=True)
        bottom_quote_df = assemble_df.sort_values(by=BaseQuote.change_ratio, ascending=True).iloc[:num].reset_index(
            drop=True)

        return top_quote_df, bottom_quote_df

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
        if not is_trade_time:
            self.__cache.set(industry_info_key, assemble_df, ttl=date_constants.HALF_HOUR_SECONDS)

        return assemble_df

    """
    :@deprecated: 获取A股指数数据
    :@param: 
    :@return: 
    """

    def fetch_a_index_info(self, v_index_code_list: []):

        index_list_str = ','.join(v_index_code_list)

        # 获取同花顺数据
        self.__ifund_client.login()
        # THS_RQ('000001.SH,399001.SZ,399006.SZ', 'latest;changeRatio;amount')
        quote = THS_RQ(index_list_str, 'latest;changeRatio;amount')

        # 处理同花顺数据，转化为df

        quote_df = quote.data
        # 登出
        self.__ifund_client.logout()

        if quote_df is None or quote_df.empty:
            raise Exception(index_list_str + '数据为空！')

        quote_df.rename(
            columns={
                'time': BaseQuote.trade_date,
                'thscode': BaseQuote.code,
                'latest': BaseQuote.latest_price,
                'changeRatio': BaseQuote.change_ratio,
                'amount': BaseQuote.amount
            },
            inplace=True)

        # 转换为交易日
        quote_df[BaseQuote.trade_date] = quote_df[BaseQuote.trade_date].map(
            lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        )

        return quote_df

    """
    :@deprecated: 获取沪港数据
    :@param: 
    :@return: 
    """

    def fetch_a_to_hk_info(self, v_name: str):
        # 获取同花顺数据
        self.__ifund_client.login()
        # THS_RQ('000001.SH,399001.SZ,399006.SZ', 'latest;changeRatio;volume')
        quote = THS_DP('balanceOfSHSZHK', '最新;最新;' + v_name, 'tradeDate:Y,updateTime:Y,buyAmount:Y,sellAmount:Y')

        # 处理同花顺数据，转化为df

        quote_df = pd.DataFrame(data=quote.data)
        # 登出
        self.__ifund_client.logout()

        if quote_df is None or quote_df.empty:
            raise Exception(v_name + '数据为空！')

        # latest_df = quote_df[quote_df['updateTime'] == '15:00'].copy()

        latest_df = pd.DataFrame([quote_df.iloc[-1].copy().to_dict()])

        if latest_df is None or latest_df.empty:
            raise Exception('当天未生成最新的' + v_name + '数据！')

        latest_df.rename(
            columns={
                'tradeDate': BaseQuote.trade_date,
                'buyAmount': BaseQuote.buy_amount,
                'sellAmount': BaseQuote.sell_amount
            },
            inplace=True)

        # 转换为交易日
        latest_df[BaseQuote.trade_date] = latest_df[BaseQuote.trade_date].map(lambda x: x.replace('/', ''))

        return latest_df

# index_code_list = ['000001.SH', '399001.SZ', '399006.SZ']
#
# test_quote = IFundQuote()
# # data_df = test_quote.fetch_a_index_info(index_code_list)
#
# HK_TO_SZ = '深股通'
# HK_TO_SH = '沪股通'
#
# HK_TO_SZ_df = test_quote.fetch_a_to_hk_info(HK_TO_SZ)
# HK_TO_SH_df = test_quote.fetch_a_to_hk_info(HK_TO_SH)

# data_df = test_quote.fetch_index_base_quote(business_config.SW_SECOND_INDUSTRY_IFUND)
