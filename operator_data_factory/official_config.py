# -*- coding: UTF-8 -*-
"""
@Description : 官网数据配置
@Author      : Jason_Sam
@Time        : 2021/4/13 11:04

"""

class HKexConfig:
    # 沪港通url
    hk_to_sh_url = 'https://sc.hkex.com.hk/TuniS/www.hkex.com.hk/chi/csm/script/data_NBSH_Turnover_chi.js?_='
    # 深港通url
    hk_to_sz_url = 'https://sc.hkex.com.hk/TuniS/www.hkex.com.hk/chi/csm/script/data_NBSZ_Turnover_chi.js?_='

class SHexConfig:
    # 上交所完整数据 http://yunhq.sse.com.cn:32041//v1/sh1/snap/000001?callback=jQuery112404269740831752953_1618290681693&select=name%2Clast%2Cchg_rate%2Cchange%2Camount%2Cvolume%2Copen%2Cprev_close%2Cask%2Cbid%2Chigh%2Clow%2Ctradephase&_=1618290681698
    quote_url_prefix = 'http://yunhq.sse.com.cn:32041//v1/sh1/snap/'
    quote_url_suffix = '?callback=jQuery112402354430016533242_1618222283811&select=name%2Clast%2Cchg_rate%2Camount&_='

class SZexConfig:
    # 深交所行情数据
    quote_url = sz_index = 'http://www.szse.cn/api/market/ssjjhq/getTimeData?random=0.2174058091008182&marketId=1&code='
