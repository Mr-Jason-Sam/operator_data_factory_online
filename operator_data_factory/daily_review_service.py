# -*- coding: UTF-8 -*-
"""
@Description : 每日收评
@Author      : Jason_Sam
@Time        : 2021/4/15 14:22

"""
import sys
import time

import business_config
import business_tools
import date_constants
import hkex
import shex
import szex
import time_tools
from base_quote import BaseQuote
from cache import BusinessCache
from ifund_quote import IFundQuote


class DailyReviewService:

    def __init__(self):
        self.__cache = BusinessCache().get_cache()
        self.__ifund_quote_service = IFundQuote()

    """
    :@deprecated: 获取三大指数数据
    :@param:
    :@return:
    """

    def fetch_base_index_quote(self, date_time: str = None):
        key = sys._getframe().f_code.co_name
        is_trade_time = business_tools.is_trade()

        # 非交易时间可使用缓存数据
        if not is_trade_time:
            index_quote_list = self.__cache.get(key)
            if index_quote_list is not None:
                return index_quote_list

        if date_time is None:
            # 获取当前毫秒级时间戳
            date_time = str(time_tools.get_now_timestamp(time_tools.TimeUnit.millisecond))

        hk_to_sh = hkex.fetch_hk_to_sh(date_time)
        hk_to_sz = hkex.fetch_hk_to_sz(date_time)

        # 获取上交所的上证指数数据
        sh_index_quote = shex.fetch_quote_info(code=business_config.SH_CODE, date_time=date_time)

        # 获取深交所的深证成指和创业板指数据
        sz_index = szex.fetch_latest_quote_info(code=business_config.SZ_CODE)
        business_index = szex.fetch_latest_quote_info(code=business_config.BS_CODE)

        trade_date = time.strftime(time_tools.TimeFormat.yyyy_mm_dd, time.localtime(int(date_time) / 1000))

        index_quote_list = list()

        # 上证指数
        index_quote_list.append(
            {
                BaseQuote.trade_date: trade_date,
                BaseQuote.code: business_config.SH_CODE,
                BaseQuote.name: sh_index_quote[0],
                BaseQuote.latest_price: sh_index_quote[1],
                BaseQuote.change_ratio: sh_index_quote[2],
                BaseQuote.amount: sh_index_quote[3] / (10 ** 8)
            }
        )

        # 深证成指
        index_quote_list.append(
            {
                BaseQuote.trade_date: trade_date,
                BaseQuote.code: business_config.SZ_CODE,
                BaseQuote.name: sz_index[0],
                BaseQuote.latest_price: sz_index[1],
                BaseQuote.change_ratio: sz_index[2],
                BaseQuote.amount: sz_index[3] / (10 ** 8)
            }
        )

        # 创业板指
        index_quote_list.append(
            {
                BaseQuote.trade_date: trade_date,
                BaseQuote.code: business_config.BS_CODE,
                BaseQuote.name: business_index[0],
                BaseQuote.latest_price: business_index[1],
                BaseQuote.change_ratio: business_index[2]
            }
        )

        # 沪港通
        index_quote_list.append(
            {
                BaseQuote.trade_date: trade_date,
                BaseQuote.code: business_config.HK_TO_SH_CODE,
                BaseQuote.name: business_config.HK_TO_SH_NAME,
                BaseQuote.buy_amount: hk_to_sh[0] / (10 ** 2),
                BaseQuote.sell_amount: hk_to_sh[1] / (10 ** 2)
            }
        )

        # 深港通
        index_quote_list.append(
            {
                BaseQuote.trade_date: trade_date,
                BaseQuote.code: business_config.HK_TO_SZ_CODE,
                BaseQuote.name: business_config.HK_TO_SZ_NAME,
                BaseQuote.buy_amount: hk_to_sz[0] / (10 ** 2),
                BaseQuote.sell_amount: hk_to_sz[1] / (10 ** 2)
            }
        )

        if not is_trade_time:
            self.__cache.set(key, index_quote_list, ttl=date_constants.ONE_DATE_SECONDS)

        return index_quote_list

    """
    :@deprecated: 获取三大指数数据
    :@param:
    :@return:
    """

    def fetch_latest_index_quote_from_ifund(self, date_time: str = None):
        key = sys._getframe().f_code.co_name
        is_trade_time = business_tools.is_trade()

        # 非交易时间可使用缓存数据
        if not is_trade_time:
            index_quote_list = self.__cache.get(key)
            if index_quote_list is not None:
                return index_quote_list

        if date_time is None:
            # 获取当前毫秒级时间戳
            date_time = str(time_tools.get_now_timestamp(time_tools.TimeUnit.millisecond))

        # 沪港通数据
        hk_to_sh_df = self.__ifund_quote_service.fetch_a_to_hk_info(v_name=business_config.IFUND_HK_TO_SH_CODE)

        # 深港通数据
        hk_to_sz_df = self.__ifund_quote_service.fetch_a_to_hk_info(v_name=business_config.IFUND_HK_TO_SZ_CODE)

        index_code_list = [business_config.IFUND_SH_CODE, business_config.IFUND_SZ_CODE, business_config.IFUND_BS_CODE]

        index_df = self.__ifund_quote_service.fetch_a_index_info(index_code_list)

        # 上证综指数据
        sh_index_df = index_df[index_df[BaseQuote.code] == business_config.IFUND_SH_CODE].copy()

        # 深证综指数据
        sz_index_df = index_df[index_df[BaseQuote.code] == business_config.IFUND_SZ_CODE].copy()

        # 创业扳指数据
        bs_index_df = index_df[index_df[BaseQuote.code] == business_config.IFUND_BS_CODE].copy()

        index_quote_list = list()

        # 上证指数
        if not sh_index_df.empty:
            sh_index_row = sh_index_df.iloc[0]
            index_quote_list.append(
                {
                    BaseQuote.trade_date: sh_index_row[BaseQuote.trade_date],
                    BaseQuote.code: business_config.SH_CODE,
                    BaseQuote.name: business_config.SH_NAME,
                    BaseQuote.latest_price: sh_index_row[BaseQuote.latest_price],
                    BaseQuote.change_ratio: round(sh_index_row[BaseQuote.change_ratio], 2),
                    BaseQuote.amount: sh_index_row[BaseQuote.amount] / (10 ** 8)
                }
            )

        # 深证成指
        if not sz_index_df.empty:
            sz_index_row = sz_index_df.iloc[0]
            index_quote_list.append(
                {
                    BaseQuote.trade_date: sz_index_row[BaseQuote.trade_date],
                    BaseQuote.code: business_config.SZ_CODE,
                    BaseQuote.name: business_config.SZ_NAME,
                    BaseQuote.latest_price: sz_index_row[BaseQuote.latest_price],
                    BaseQuote.change_ratio: round(sz_index_row[BaseQuote.change_ratio], 2),
                    BaseQuote.amount: sz_index_row[BaseQuote.amount] / (10 ** 8)
                }
            )

        # 创业板指
        if not bs_index_df.empty:
            bs_index_row = bs_index_df.iloc[0]
            index_quote_list.append(
                {
                    BaseQuote.trade_date: bs_index_row[BaseQuote.trade_date],
                    BaseQuote.code: business_config.BS_CODE,
                    BaseQuote.name: business_config.BS_NAME,
                    BaseQuote.latest_price: bs_index_row[BaseQuote.latest_price],
                    BaseQuote.change_ratio: round(bs_index_row[BaseQuote.change_ratio], 2),
                    BaseQuote.amount: bs_index_row[BaseQuote.amount] / (10 ** 8)
                }
            )

        # 沪股通
        if not hk_to_sh_df.empty:
            hk_to_sh_row = hk_to_sh_df.iloc[0]
            index_quote_list.append(
                {
                    BaseQuote.trade_date: hk_to_sh_row[BaseQuote.trade_date],
                    BaseQuote.code: business_config.HK_TO_SH_CODE,
                    BaseQuote.name: business_config.HK_TO_SH_NAME,
                    BaseQuote.buy_amount: hk_to_sh_row[BaseQuote.buy_amount],
                    BaseQuote.sell_amount: hk_to_sh_row[BaseQuote.sell_amount]
                }
            )

        # 沪股通
        if not hk_to_sz_df.empty:
            hk_to_sz_row = hk_to_sz_df.iloc[0]
            index_quote_list.append(
                {
                    BaseQuote.trade_date: hk_to_sz_row[BaseQuote.trade_date],
                    BaseQuote.code: business_config.HK_TO_SZ_CODE,
                    BaseQuote.name: business_config.HK_TO_SZ_NAME,
                    BaseQuote.buy_amount: hk_to_sz_row[BaseQuote.buy_amount],
                    BaseQuote.sell_amount: hk_to_sz_row[BaseQuote.sell_amount]
                }
            )

        if not is_trade_time:
            self.__cache.set(key, index_quote_list, ttl=date_constants.ONE_DATE_SECONDS)

        return index_quote_list
