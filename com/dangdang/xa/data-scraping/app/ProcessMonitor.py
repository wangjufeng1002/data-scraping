#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 1.数据库获取所有超过一分钟状态为1的数据。 2.根据数据行的进程ID进行核实 3.未存在运行 改库  或者超时干掉进程 改库

import psutil
import datetime
import time
from pymysql_comm import UsingMysql




def monitor_start():
    result = queryData()
    print("..........result='{}'".format(result))
    if result == None:
        print("..........result='{}'............".format(result))
        return
    else:
        for re in result:
            print(".......re='{}'。。。。。。。".format(re))
            pport = re['port']
            print("pid='{}'......".format(pport))
            if(get_process("chrome.exe",re['port']) is True):
                print("true..................")


def tt():
    get_process_tt("chrome.exe")
    #if(get_process("chrome.exe",2408) is True):



def queryData():
    with UsingMysql() as um:
        sql = "select id,pid from account_info where run_status='1'  and  SUBDATE(update_time,INTERVAL 1 MINUTE)"
        um.cursor.execute(sql)
        data = um.cursor.fetchall()
        return data

def updateData():
    with UsingMysql() as um:
        sql = "update account_info set run_status=0 where run_status = 1 and `status` = 1 and  SUBDATE(update_time,INTERVAL 30 MINUTE)"
        um.cursor.execute(sql)

def get_process(pname,runPid):
    for proc in psutil.process_iter():
        sname = proc.name()
        spid = proc.pid
        if sname == pname and spid == int(runPid):
            curr = time.time()
            ptime = proc.create_time()
            #进程一直活着 但超过5分钟 就强行杀死 改库  从新运行。一般都是进程死了，直接返回改库
            if (datetime.datetime.fromtimestamp(curr) -datetime.datetime.fromtimestamp(ptime)).seconds > 1800:
                print("进程='{}',进程号='{}',启动时间='{}',超时杀死进程".format(sname,spid,datetime.datetime.fromtimestamp(ptime)))
                return True
            else:
                print("进程='{}',进程号='{}',未超时再等等".format(sname,spid))
                return False
    return True

def get_process_tt(pname):
    for proc in psutil.process_iter():
        if proc.name() == pname:
            get_process(pname);



if __name__ == '__main__':
    #monitor_start()
    get_process("chrome.exe","11536")

