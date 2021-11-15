"""
@Description : 收盘数据
@Author      : Jason_Sam
@Time        : 2021/4/16 17:20

"""


class CloseMktInfo:
    trade_date: str = 'trade_date'

    sh_name: str = 'sh_name'
    sh_change: str = 'sh_change'
    sh_price: str = 'sh_price'
    sh_amount: str = 'sh_amount'

    sz_name: str = 'sz_name'
    sz_change: str = 'sz_change'
    sz_price: str = 'sz_price'
    sz_amount: str = 'sz_amount'

    bs_name: str = 'bs_name'
    bs_change: str = 'bs_change'
    bs_price: str = 'bs_price'

    sh_sz_trade_amount: str = 'sh_sz_trade_amount'
    north_net_amount: str = 'north_net_amount'

    hk_to_sh_code: str = 'hk_to_sh_code'
    hk_to_sh_amount: str = 'hk_to_sh_amount'
    hk_to_sz_code: str = 'hk_to_sz_code'
    hk_to_sz_amount: str = 'hk_to_sz_amount'

    top_industry: str = 'top_industry'
    bottom_industry: str = 'bottom_industry'
