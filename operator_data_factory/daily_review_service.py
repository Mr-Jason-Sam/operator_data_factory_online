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
import hkex
import shex
import szex
import time_tools
from base_quote import BaseQuote
from cache import BusinessCache


class DailyReviewService:

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
            index_quote_list = BusinessCache().get_cache().get(key)
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
            BusinessCache().get_cache().set(key, index_quote_list)

        return index_quote_list

