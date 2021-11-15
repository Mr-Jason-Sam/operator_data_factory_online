# -*- coding: UTF-8 -*-
"""
@Description : 指数数据
@Author      : Jason_Sam
@Time        : 2021/4/26 17:52

"""
from base_quote import BaseQuote
from business_db_config import BusinessDbConfig


def handle_sql_data(dict_data, key):
    try:
        if dict_data[key] is None:
            return 'null'
        return "'" + str(dict_data[key]) + "'"
    except KeyError:
        return 'null'


class IndexMapper:

    def __init__(self):
        self.__business_cfg = BusinessDbConfig()
        self.__cursor = self.__business_cfg.get_cursor()
        self.__connection = self.__business_cfg.get_connection()

    """
    :@deprecated: 存储指数数据
    :@param: 
    :@return: 
    """
    def save_index_data(self, data_list: list):
        if data_list is None or not data_list:
            raise Exception('指数数据为空')

        for data in data_list:
            merge_into_sql = """
                MERGE INTO INDEX_QUOTE_INFO QUOTE_INFO
                USING (
                    SELECT """ + handle_sql_data(data, BaseQuote.code) + """ INDEX_CODE, """ + handle_sql_data(data, BaseQuote.trade_date) + """ TRADE_DT,
                    """ + handle_sql_data(data, BaseQuote.latest_price) + """ INDEX_PRICE, """ + handle_sql_data(data, BaseQuote.change_ratio) + """ INDEX_CHANGE,
                    """ + handle_sql_data(data, BaseQuote.name) + """ INDEX_NAME,
                    """ + handle_sql_data(data, BaseQuote.buy_amount) + """ INDEX_BUY_AMOUNT, """ + handle_sql_data(data, BaseQuote.sell_amount) + """ INDEX_SELL_AMOUNT
                    FROM DUAL
                ) QUOTE_DATA
                ON (
                        QUOTE_INFO.CODE = QUOTE_DATA.INDEX_CODE AND QUOTE_INFO.TRADE_DATE = QUOTE_DATA.TRADE_DT
                    )
                WHEN MATCHED THEN
                    UPDATE
                    SET QUOTE_INFO.PRICE       = QUOTE_DATA.INDEX_PRICE,
                        QUOTE_INFO.CHANGE      = QUOTE_DATA.INDEX_CHANGE,
                        QUOTE_INFO.NAME        = QUOTE_DATA.INDEX_NAME,
                        QUOTE_INFO.BUY_AMOUNT  = QUOTE_DATA.INDEX_BUY_AMOUNT,
                        QUOTE_INFO.SELL_AMOUNT = QUOTE_DATA.INDEX_SELL_AMOUNT,
                        QUOTE_INFO.UPDATE_TIME = SYSDATE
                WHEN NOT MATCHED THEN
                    INSERT (QUOTE_INFO.CODE, QUOTE_INFO.TRADE_DATE, QUOTE_INFO.PRICE, QUOTE_INFO.CHANGE, QUOTE_INFO.NAME,
                            QUOTE_INFO.BUY_AMOUNT, QUOTE_INFO.SELL_AMOUNT)
                    VALUES (QUOTE_DATA.INDEX_CODE, QUOTE_DATA.TRADE_DT, QUOTE_DATA.INDEX_PRICE, QUOTE_DATA.INDEX_CHANGE, QUOTE_DATA.INDEX_NAME,
                            QUOTE_DATA.INDEX_BUY_AMOUNT, QUOTE_DATA.INDEX_SELL_AMOUNT)
            """
            self.__cursor.execute(merge_into_sql)

        self.__connection.commit()


    """
    :@deprecated: 保存板块数据
    :@param: 
    :@return: 
    """
    def save_industry_data(self, data_list):
        if data_list is None or not data_list:
            raise Exception('板块数据为空')

        for data in data_list:
            merge_into_sql = """
                MERGE INTO INDUSTRY_QUOTE_INFO QUOTE_INFO
                USING (
                    SELECT """ + handle_sql_data(data, BaseQuote.code) + """ INDEX_CODE, """ + handle_sql_data(data, BaseQuote.trade_date) + """ TRADE_DT,
                    """ + handle_sql_data(data, BaseQuote.change_ratio) + """ INDEX_CHANGE, """ + handle_sql_data(data, BaseQuote.name) + """ INDEX_NAME,
                    """ + handle_sql_data(data, BaseQuote.latest_price) + """ INDEX_PRICE
                    FROM DUAL
                ) QUOTE_DATA
                ON (
                        QUOTE_INFO.CODE = QUOTE_DATA.INDEX_CODE AND QUOTE_INFO.TRADE_DATE = QUOTE_DATA.TRADE_DT
                    )
                WHEN MATCHED THEN
                    UPDATE
                    SET QUOTE_INFO.CHANGE = QUOTE_DATA.INDEX_CHANGE,
                        QUOTE_INFO.NAME   = QUOTE_DATA.INDEX_NAME,
                        QUOTE_INFO.PRICE   = QUOTE_DATA.INDEX_PRICE,
                        QUOTE_INFO.UPDATE_TIME = SYSDATE
                WHEN NOT MATCHED THEN
                    INSERT (QUOTE_INFO.CODE, QUOTE_INFO.TRADE_DATE, QUOTE_INFO.CHANGE, QUOTE_INFO.NAME, QUOTE_INFO.PRICE)
                    VALUES (QUOTE_DATA.INDEX_CODE, QUOTE_DATA.TRADE_DT, QUOTE_DATA.INDEX_CHANGE, QUOTE_DATA.INDEX_NAME, QUOTE_DATA.INDEX_PRICE)
            """
            self.__cursor.execute(merge_into_sql)

        self.__connection.commit()
