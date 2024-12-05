#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import os.path
import sys
import time
import datetime

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
import instock.lib.run_template as runt
import instock.core.tablestructure as tbs
import instock.lib.database as mdb
import instock.core.stockfetch as stf
from instock.lib.logger import log_execution_details

__author__ = 'myh '
__date__ = '2023/3/10 '


# 每日股票大宗交易
@log_execution_details
def save_after_close_stock_blocktrade_data(date):
    try:
        data = stf.fetch_stock_blocktrade_data(date)
        if data is None or len(data.index) == 0:
            return

        table_name = tbs.TABLE_CN_STOCK_BLOCKTRADE['name']
        # 删除老数据。
        if mdb.checkTableIsExist(table_name):
            del_sql = f"DELETE FROM `{table_name}` where `date` = '{date}'"
            mdb.executeSql(del_sql)
            cols_type = None
        else:
            cols_type = tbs.get_field_types(tbs.TABLE_CN_STOCK_BLOCKTRADE['columns'])

        mdb.insert_db_from_df(data, table_name, cols_type, False, "`date`,`code`")
    except Exception as e:
        logging.error(f"basic_data_other_daily_job.save_stock_blocktrade_data处理异常：{e}")


def main():
    start = time.time()
    _start = datetime.datetime.now()
    logging.info("######## basic_data_after_close_daily_job 任务执行时间: %s #######" % _start.strftime("%Y-%m-%d %H:%M:%S.%f"))

    runt.run_with_args(save_after_close_stock_blocktrade_data)

    logging.info("######## basic_data_after_close_daily_job 完成任务, 使用时间: %s 秒 #######" % (time.time() - start))


# main函数入口
if __name__ == '__main__':
    main()
