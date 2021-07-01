from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
import threading, time
import process


# 根据cookies 数并发执行线程
# nohup python getItemDetailData.py  >nohup.log 2>&1 &
# nohup python getItemDetailDataCurrent.py  > logs/nohup-current.log 2>&1 &
def processAll():
    logUtils = Logger(filename='./logs/detail.log', level='info')
    dataReptiledb.init(None, "./logs/db-all.log")
    categorys = dataReptiledb.getNotDealCategory()
    headers = dataReptiledb.getHeaders(None)
    if categorys is None or len(categorys) <= 0:
        logUtils.logger.info("未找到需要处理的分类")
        raise Exception("未找到需要处理的分类")
    if headers is None or len(headers) <= 0:
        logUtils.logger.info("未找到headers")
        raise Exception("未找到headers")
    index = 0
    for header in headers:
        if index < len(categorys):
            threading.Thread(target=process.processBookInfo, args=(categorys[index], header),
                             name=categorys[index]).start()
            index += 1
        else:
            logUtils.logger.info("线程启动结束")


def processPromo(headers, categorys):
    logUtils = Logger(filename='./logs/detail-current.log', level='info')
    dataReptiledb.init(None, "./logs/db-current.log")
    # categorys = dataReptiledb.getNotDealCategoryByBook()
    # headers = dataReptiledb.getHeaders()
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
            threading.Thread(target=process.processBookPromoInfo, args=(categorys[index], headers[headerIndex]),
                             name="自定义<->" + categorys[index] + "<->" + headers[headerIndex].get("account")).start()
            # 每个账号绑定一个分类
            threadParamMap[headers[headerIndex].get("account")] = categorys[index]
            index += 1
        else:
            logUtils.logger.info("线程启动结束")
    return threadParamMap


if __name__ == '__main__':
    logUtils = Logger(filename='./logs/detail-current.log', level='info')
    dataReptiledb.init(None, "./logs/db-current.log")

    categorys = dataReptiledb.getNotDealCategoryByBook()
    # 查询 cookies
    headers = dataReptiledb.getHeaders(None)
    if categorys is None or headers is None:
        logUtils.logger.error("未找到需要处理的分类")
        raise Exception("未找到需要处理的分类")
    # 开始处理
    processPromo(headers, categorys)

    while True:
        threadParamMap ={}
        time.sleep(3)
        custThreadCnt = 0
        threads = threading.enumerate()
        for thread in threads:
            if "自定义" in thread.name:
                custThreadCnt += 1
                split = thread.name.split("<->")
                threadParamMap[split[2]]=split[1]
        # 当前正在执行的线程数 与 绑定的线程数相等，没有线程结束
        headers = dataReptiledb.getHeaders(None)
        freeHeaders = []
        for tempHeader in headers:
            acc = tempHeader.get("account")
            # 当前cookie 不在运行的 线程中绑定
            if threadParamMap.get(acc) is None:
                freeHeaders.append(tempHeader)
        # 排除正在运行的分类
        categorys = dataReptiledb.getNotDealCategoryByBook()
        runCategorys = threadParamMap.values()
        #得到未执行的分类
        freeCategorys = list(set(categorys).difference(set(runCategorys)))
        if freeHeaders is not None and len(freeHeaders) != 0 and freeCategorys is not None and len(freeCategorys) !=0:
            logUtils.logger.info("准备新启线程{size}".format(size=len(freeHeaders)))
            processPromo(freeHeaders, freeCategorys)