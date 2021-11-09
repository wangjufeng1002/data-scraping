#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 1.数据库获取所有超过一分钟状态为1的数据。 2.根据数据行的进程ID进行核实 3.未存在运行 改库

import psutil
import datetime
import time
import logging
import pymysql
import socket
from timeit import default_timer

#-----------------------日志输出----------------------

class MonitorLogger:
    def __init__(self, loggername):
        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.INFO)

        time = datetime.datetime.now().strftime("%Y-%m-%d")
        # 创建一个handler，用于写入日志文件
        log_path = r'.\monlog\\'  # 指定文件输出路径，注意logs是个文件夹，一定要加上/，不然会导致输出路径错误，把logs变成文件名的一部分了
        logname = log_path + time + '.log'  # 指定输出的日志文件名
        fh = logging.FileHandler(logname, encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(logging.INFO)

        # 创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger


log = MonitorLogger('MON').get_log()
#------------------数据库连接----------------

host = '10.7.40.197'
port = 9174
db = 'data_scraping'
user = 'data_scraping_rw'
password = 'my@#6VIDwc1vRW'


# ---- 用pymysql 操作数据库
def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


# ---- 使用 with 的方式来优化代码
class UsingMysql(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 在进入的时候自动获取连接和cursor
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._conn.commit()
        # 在退出的时候自动关闭连接和cursor
        self._cursor.close()
        self._conn.close()
    @property
    def cursor(self):
        return self._cursor


#-----------------程序方法-----------------

def monitor_start():
    currhost = socket.gethostname()
    currIp = socket.gethostbyname(currhost)
    #程序不能乱跑   必须是当前执行机器
    result = queryData(currIp)
    processions = get_process_run_count("python.exe")
    try:
        if len(result) == 0:
            log.info("....python.exe....此进程....目前启动....{}....个....".format(processions))
            return
        else:
            for re in result:
                if (get_process("python.exe", re['pid'],re['port'],re['update_time']) is True):
                    updateData(re['id'])
        log.info("...python.exe...此进程...目前启动...{}...个...".format(processions))
    except:
        log.info("++++++定时检测进程,程序执行异常------")


def queryData(runIp):
    with UsingMysql() as um:
        sql = "select id,pid,port,update_time from account_info where run_status='1' and status=1  and  SUBDATE(update_time,INTERVAL 1 MINUTE) and ip='{}'".format(runIp)
        um.cursor.execute(sql)
        data = um.cursor.fetchall()
        return data


def updateData(iid):
    with UsingMysql() as um:
        sql = "update account_info set run_status='0',last_modified_time=now() where id={} and run_status ='1'".format(iid)
        um.cursor.execute(sql)
        um._conn.commit()


def get_process(pname, runPid, port, uptime):
    for proc in psutil.process_iter():
        sname = proc.name()
        spid = proc.pid
        if sname == pname and spid == int(runPid):
            curr = time.time()
            ptime = proc.create_time()
            #数据库更新时间间隔2分钟,直接杀掉进程 重启
            if (datetime.datetime.fromtimestamp(curr) - datetime.datetime.fromtimestamp(uptime)).seconds > 120:
                log.info("手机='{}',进程号='{}',上次更新时间='{}',距离上次更新时间超过2分钟,强杀进程".format(port, spid, datetime.datetime.fromtimestamp(uptime)))
                proc.kill(spid)
                return True
            # 进程一直活着 但超过一定时间 打个日志标识下 不进行处理
            if (datetime.datetime.fromtimestamp(curr) - datetime.datetime.fromtimestamp(ptime)).seconds > 600:
                log.info("手机='{}',进程号='{}',启动时间='{}',长时间稳定运行,做个记录".format(port, spid,datetime.datetime.fromtimestamp(ptime)))
                return False
    log.info("手机='{}',记录进程号='{}',该进程不存在,但是数据库状态为1,需要更新数据库".format(port, runPid))
    return True

def get_process_run_count(pname):
    count = 0
    for proc in psutil.process_iter():
        sname = proc.name()
        if sname == pname:
            count = count+1
    return count


# ------------------------启动入口--------------------------

if __name__ == '__main__':
    monitor_start()
