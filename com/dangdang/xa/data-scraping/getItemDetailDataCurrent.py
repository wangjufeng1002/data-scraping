from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
import threading, time
import process




#根据cookies 数并发执行线程
#nohup python getItemDetailData.py  >nohup.log 2>&1 &
#nohup python getItemDetailDataCurrent.py  > logs/nohup-current.log 2>&1 &
def processAll():
    logUtils = Logger(filename='./logs/detail.log', level='info')
    dataReptiledb.init(None, "./logs/db-all.log")
    categorys = dataReptiledb.getNotDealCategory()
    headers = dataReptiledb.getHeaders()
    if categorys is None or len(categorys)<=0:
        logUtils.logger.info("未找到需要处理的分类")
        raise Exception("未找到需要处理的分类")
    if headers is None or len(headers)<=0:
        logUtils.logger.info("未找到headers")
        raise Exception("未找到headers")
    index = 0
    for header in headers:
        if index < len(categorys):
            threading.Thread(target=process.processBookInfo, args=(categorys[index], header),name=categorys[index]).start()
            index+=1
        else:
            logUtils.logger.info("线程启动结束")
def processPromo():
    logUtils = Logger(filename='./logs/detail-current.log', level='info')
    dataReptiledb.init(None,"./logs/db-current.log")
    categorys = dataReptiledb.getNotDealCategoryByBook()
    headers = dataReptiledb.getHeaders()
    if categorys is None or len(categorys) <= 0:
        logUtils.logger.info("未找到需要处理的分类")
        raise Exception("未找到需要处理的分类")
    if headers is None or len(headers) <= 0:
        logUtils.logger.info("未找到headers")
        raise Exception("未找到headers")
    index = 0
    headersIndex = 0
    for headerIndex in range(0,len(headers)):
        if index < len(categorys):
            threading.Thread(target=process.processBookPromoInfo, args=(categorys[index], headersIndex),
                                             name=categorys[index]).start()
            index += 1
        else:
            logUtils.logger.info("线程启动结束")
if __name__ == '__main__':
    processPromo()