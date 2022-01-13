# -*- coding: UTF-8 -*-
"""
@Description : 业务任务
@Author      : Jason_Sam
@Time        : 2021/4/28 10:20

"""
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from index_mapper import IndexMapper
from quote_controller import QuoteController

scheduler = BlockingScheduler()

logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='log/business_job.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


def close_market_job():
    quote_controller = QuoteController()
    index_quote_data = quote_controller.get_index_base_quote()
    industry_quote_data = quote_controller.get_industry()

    data_dict = industry_quote_data.to_dict(orient='records')

    index_mp = IndexMapper()

    index_mp.save_index_data(index_quote_data)
    index_mp.save_industry_data(data_dict)

    logging.info('CloseMarketJob Success！')
    print('Success')


if __name__ == '__main__':
    close_market_job()
    # 收盘任务
    scheduler.add_job(
         close_market_job,
         trigger=CronTrigger(hour=15, minute='5/5', day_of_week='mon-fri')
    )
    
    logging.info('close_market_job start！')
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
