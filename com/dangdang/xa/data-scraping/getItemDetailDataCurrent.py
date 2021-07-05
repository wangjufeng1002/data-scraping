from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
import threading, time
import process
import sys, getopt



# 根据cookies 数并发执行线程
# nohup python getItemDetailData.py  -a 1  >nohup.log 2>&1 &
# nohup python getItemDetailDataCurrent.py -a 2  >> logs/nohup-current.log 2>&1 &
def processAll(headers, categorys,logUtils):
    dataReptiledb.init(None, "./logs/db-current.log")
    if categorys is None or len(categorys) <= 0:
        logUtils.logger.error("未找到需要处理的分类")
        raise Exception("未找到需要处理的分类")
    if headers is None or len(headers) <= 0:
        logUtils.logger.error("未找到headers")
        raise Exception("未找到headers")
    threadParamMap = {}
    index = 0
    for headerIndex in range(0, len(headers)):
        if index < len(categorys):
            threading.Thread(target=process.processBookInfo, args=(categorys[index], headers[headerIndex],logUtils),
                             name="自定义<->" + categorys[index] + "<->" + headers[headerIndex].get("account")).start()
            # 每个账号绑定一个分类
            threadParamMap[headers[headerIndex].get("account")] = categorys[index]
            index += 1
        else:
            logUtils.logger.info("线程启动结束")
    return threadParamMap


def processPromo(headers, categorys, logUtils):
    dataReptiledb.init(None, "./logs/db-current.log")
    if categorys is None or len(categorys) <= 0:
        logUtils.logger.error("未找到需要处理的分类")
        raise Exception("未找到需要处理的分类")
    if headers is None or len(headers) <= 0:
        logUtils.logger.error("未找到headers")
        raise Exception("未找到headers")
    threadParamMap = {}
    index = 0
    for headerIndex in range(0, len(headers)):
        if index < len(categorys):
            threading.Thread(target=process.processBookPromoInfo, args=(categorys[index], headers[headerIndex],logUtils),
                             name="自定义<->" + categorys[index] + "<->" + headers[headerIndex].get("account")).start()
            # 每个账号绑定一个分类
            threadParamMap[headers[headerIndex].get("account")] = categorys[index]
            index += 1
        else:
            logUtils.logger.info("线程启动结束")
    return threadParamMap


def auto_process(flag):
    logUtils = Logger(filename='./logs/detail-current.log', level='info')
    dataReptiledb.init(None, "./logs/db-current.log")
    categorys = dataReptiledb.getNotDealCategoryByBook()
    # 查询 cookies
    headers = dataReptiledb.getHeaders(None)
    if categorys is None or headers is None:
        logUtils.logger.error("未找到需要处理的分类")
        raise Exception("未找到需要处理的分类")
    # 开始处理
    if flag == 1:
        processPromo(headers=headers, categorys=categorys, logUtils=logUtils)
    if flag == 2:
        processAll(headers=headers, categorys=categorys, logUtils=logUtils)
    while True:
        try:
            threadParamMap = {}
            time.sleep(10)
            custThreadCnt = 0
            threads = threading.enumerate()
            for thread in threads:
                if "自定义" in thread.name:
                    custThreadCnt += 1
                    split = thread.name.split("<->")
                    threadParamMap[split[2]] = split[1]
            # 当前正在执行的线程数 与 绑定的线程数相等，没有线程结束
            headers = dataReptiledb.getHeaders(None)
            freeHeaders = []
            for tempHeader in headers:
                acc = tempHeader.get("account")
                # 当前cookie 不在运行的 线程中绑定
                if threadParamMap.get(acc) is None:
                    freeHeaders.append(tempHeader)
            if len(freeHeaders) == 0:
                continue
            # 排除正在运行的分类
            categorys = dataReptiledb.getNotDealCategoryByBook()
            runCategorys = threadParamMap.values()
            # 得到未执行的分类
            freeCategorys = list(set(categorys).difference(set(runCategorys)))
            if freeHeaders is not None and len(freeHeaders) != 0 and freeCategorys is not None and len(
                    freeCategorys) != 0:
                logUtils.logger.info("准备新启线程{size}".format(size=len(freeHeaders)))
                if flag == 1:
                    processPromo(freeHeaders, freeCategorys,logUtils=logUtils)
                if flag == 2:
                    processAll(freeHeaders,freeCategorys,logUtils=logUtils)
        except Exception as e:
            logUtils.logger.error("线程检测出现异常")
            logUtils.logger.error(u"线程检测出现异常", e, exc_info=True, stack_info=True)


if __name__ == '__main__':
    active = 1
    opts, args = getopt.getopt(sys.argv[1:], "a:")
    for opt, arg in opts:
        if opt == "-a":
            active = arg

    # 1. 只从book表中查出信息，更新促销信息
    #auto_process(1)
    # 2. 从item_url 查出未处理的Url,更新促销信息
    auto_process(int(active))
    # 自动
