"""
@Description : 业务数据库配置
@Author      : Jason_Sam
@Time        : 2021/4/26 17:58

"""
import cx_Oracle


class BusinessDbConfig:
    user = 'wj_oms'
    password = 'wj_oms'
    link = '10.190.0.60:1528/cjhx'

    pools = cx_Oracle.SessionPool(user, password, link, min=3, max=10, increment=1, threaded=True, encoding="UTF-8")

    def __init__(self):
        self.__connection = BusinessDbConfig.pools.acquire()

    def __del__(self):
        # Release the connection to the pool
        BusinessDbConfig.pools.release(self.__connection)
        # Close the pool
        # BusinessDbConfig.pools.close()

    def get_cursor(self):
        # busies = self.__pools.busy
        # if busies
        return self.__connection.cursor()

    def get_connection(self):
        return self.__connection
