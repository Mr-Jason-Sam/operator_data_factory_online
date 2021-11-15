"""
@Description : 指数基础行情
@Author      : Jason_Sam
@Time        : 2021/4/14 17:17

"""

class BaseQuote:
    code: str = 'CODE'
    latest_price: str = 'LATEST_PRICE'
    change_ratio: str = 'CHANGE_RATIO'
    name: str = 'NAME'
    trade_date: str = 'TRADE_DATE'
    amount: str = 'AMOUNT'
    buy_amount = 'BUY_AMOUNT'
    sell_amount = 'SELL_AMOUNT'
