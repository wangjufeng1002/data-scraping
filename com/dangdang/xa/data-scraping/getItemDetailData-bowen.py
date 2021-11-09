#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import ItemUrl, Book, Logger
import threading, time
import getItemDetailData, getIpProxyPool
#nohup python getItemDetailData-bowen.py  >nohup-bowen.log 2>&1 &
logUtils = Logger(filename='./logs/detail-bowen.log', level='info')
file_object = open('./TM/item-detail-base-bowen.txt', "a", encoding='utf-8')
def processPriceData(itemUrlEntity, ip):
    threadName= threading.current_thread().name
    session = HTMLSession()
    proxy = {'http': "http://" + ip, 'https': "https://" + ip}
    detailResponse = session.get(url=itemUrlEntity.itemUrl.replace("http", "https"), proxies=proxy, timeout=(3, 4))

    detailHtmlSoup = BeautifulSoup(detailResponse.text, features='html.parser')
    itemId = re.match(".*?(id=.*&).*", itemUrlEntity.itemUrl, re.S).group(1).split('&')[0].replace('id=', '')
    defaultPrice = re.match(".*?(\"defaultItemPrice\":.*&).*", detailResponse.text, re.S).group(1).split(',')[
        0].replace("defaultItemPrice", "").replace('\"', "").replace(":", "").replace(",", "")

    itmDescUl = detailHtmlSoup.find_all(name="ul", attrs={"id": "J_AttrUL"})
    if itmDescUl is None or len(itmDescUl) == 0:
        return
    book = Book(tmId=itemId, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                promotionPriceDesc=None, price=defaultPrice, promotionType=None, activeStartTime=None,
                activeEndTime=None,
                activeDesc=None, shopName=itemUrlEntity.shopName, category=itemUrlEntity.category, sales="0",
                press=None)
    contents = itmDescUl[0].contents
    for con in contents:
        if "书名" in con.next:
            book.setName(con.next.replace("书名: ", ""))
        if "ISBN" in con.next:
            book.setIsbn(con.next.replace("ISBN编号: ", ""))
        if ("作者" in con.next) or ("编者" in con.next):
            if "作者地区" not in con.next:
                book.setAuther(con.next.replace("作者: ", "").replace("编者: ", ""))
        if ("定价" in con.next) or ("价格" in con.next):
            book.setFixPrice(con.next.replace("定价: ", "").replace("价格: ", ""))
        if ("出版社" in con.next) or ("出版社" in con.next):
            book.setPress(con.next.replace("出版社名称:", ""))

    # 获取促销信息
    # processPromotion(book, header, ip)
    # disturbUrl(header, ip)
    # 写入数据库
    # dataReptiledb.insertDetailPrice(book)
    file_object.write(book.toString() + "\n")
    file_object.flush()
    logUtils.logger.info("{threadName} process book {id}".format(threadName=threadName,id=itemId))
    # time.sleep(5)
    # time.sleep(random.randint(2, 10))


def processBowenThread(itemUrls):
    threadName= threading.current_thread().name
    logUtils.logger.info("{threadName} 线程启动,需要处理数据量: {size}".format(threadName=threadName,size=len(itemUrls)))
    proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
    for itemUrl in itemUrls:
        try:
            processPriceData(itemUrl, ip=proxyIp)
            logUtils.logger.info("%s 处理成功 %s", threadName, itemUrl.itemId)
        except Exception as e:
            proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
            logUtils.logger.info("%s 线程出现异常 %s itemId=%s",threadName,e,itemUrl.itemId)
            pass
        # else:
        #     dataReptiledb.updateSuccessFlag(1,itemId=itemUrl.itemId)

def processBowen(shopName,size):
    threadProcessSize = 10000
    itemUrls = dataReptiledb.getItemUrlByShopName(shopName,size)
    if itemUrls is None or len(itemUrls) <= 0:
        return
    if len(itemUrls) <= 10000:
        threading.Thread(target=processBowenThread, args=(itemUrls,), name="自定义-博文线程").start()
        return
    r = int(len(itemUrls) / threadProcessSize)
    m = len(itemUrls) % threadProcessSize
    result = r + (1 if m > 0 else 0)
    logUtils.logger.info("准备启动{num} 个线程".format(num=result))
    for i in range(0, result):
        threading.Thread(target=processBowenThread, args=(itemUrls[threadProcessSize * i:threadProcessSize * (i + 1)],),
                         name="自定义-博文线程-%d" % i).start()


if __name__ == '__main__':
    processBowen(shopName="博文",size=50000)
    processBowenExecuteCnt =1

    while True:
        time.sleep(30)
        custThreadCnt = 0
        threads = threading.enumerate()
        for thread in threads:
            if "自定义" in thread.name:
                custThreadCnt+=1
        if custThreadCnt == 0:
            processBowen(shopName="博文",size=50000)
            processBowenExecuteCnt+=1
        if processBowenExecuteCnt == 5:
            break
