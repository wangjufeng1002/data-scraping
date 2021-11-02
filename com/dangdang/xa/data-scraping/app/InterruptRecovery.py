#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
程序异常终端恢复脚本
程序异常中止后，手机的运行状态无法被重置，则无法进行下一次任务
在问题解决前，利用脚本将超时无法自动恢复的手机运行状态重置
'''

import pymysql
import time

host = '10.7.40.197'
port = 9174
db = 'data_scraping'
user = 'data_scraping_rw'
password = 'my@#6VIDwc1vRW'


# ---- 用pymysql 操作数据库
def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn

def runOntime():
    with UsingMysql() as um:
        print("update interruptRecovery begin")
        sql = "update account_info set run_status=0 where run_status = 1 and `status` = 1 and  SUBDATE(update_time,INTERVAL 30 MINUTE)"
        um.cursor.execute(sql)
        print("update interruptRecovery done")




