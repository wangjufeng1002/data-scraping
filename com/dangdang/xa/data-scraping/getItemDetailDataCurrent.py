from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
import threading, time
import process




#根据cookies 数并发执行线程
if __name__ == '__main__':
    logUtils = Logger(filename='./logs/detail.log', level='info')

    categorys = dataReptiledb.getNotDealCategory()
    headers = dataReptiledb.getHeaders()
    if categorys is None or len(categorys):
        logUtils.logger.info("未找到需要处理的分类")
    if headers is None or len(headers):
        logUtils.logger.info("未找到headers")
    index = 0
    for header in headers:
        if index < len(categorys):
            processThread = threading.Thread(target=process.processPromotion, args=(categorys[index], header),
                                     name=categorys[index]).start()
            index+=1
        else:
            logUtils.logger.info("线程启动结束")