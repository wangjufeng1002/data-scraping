from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
import threading, time
import getIpProxyPool
import constants
import sys, getopt
def macth_brackets(text):
    match = re.search("TShop\\.Setup\\((.*)\\);", text, re.S)
    text = match.group(0)
    stack = []
    match_s = "("
    match_e = ")"
    jsonStr = ""
    start_index = text.find("TShop.Setup")+len("TShop.Setup")
    end_index = len(text)-1
    for i in range(start_index,end_index):
        if text[i] == match_s:
            stack.append(i)
        if text[i] == match_e:
            stack.pop()
        if len(stack) ==0:
            jsonStr = text[start_index+1:i]
            break
    return jsonStr
def processDefaultBookData(itemUrlEntity, ip, logUtils):
    proxy = {'http': "http://" + ip, 'https': "https://" + ip}
    session = HTMLSession()
    detailResponse = session.get(itemUrlEntity.itemUrl, proxies=proxy,timeout=(3,4))
    detailHtmlSoup = BeautifulSoup(detailResponse.text.encode("utf-8"), features='html.parser')
    book = Book(tmId=itemUrlEntity.itemId, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                promotionPriceDesc=None, price=None, promotionType=None, activeStartTime=None,
                activeEndTime=None,
                activeDesc="", shopName=itemUrlEntity.shopName, category=itemUrlEntity.category, sales="0", press=None)
    if "很抱歉，您查看的商品找不到了" in detailResponse.text:
        dataReptiledb.insertDetailPrice(book)
        logUtils.logger.error(
            "线程{threadName} - 商品已经下架 {id}".format(threadName=threading.current_thread().getName(), id=itemUrlEntity.itemId))
        return None,2

    itemId = re.match(".*?(id=.*&).*", itemUrlEntity.itemUrl, re.S).group(1).split('&')[0].replace('id=', '')
    defaultPrice = re.match(".*?(\"defaultItemPrice\":.*&).*", detailResponse.text, re.S).group(1).split(',')[
        0].replace("defaultItemPrice", "").replace('\"', "").replace(":", "").replace(",", "")

    book.setPrice(defaultPrice)
    itmDescUl = detailHtmlSoup.find_all(name="ul", attrs={"id": "J_AttrUL"})
    logUtils.logger.info("{itemId} {itmDescUl}".format(itemId=itemId,itmDescUl=itmDescUl))
    if itmDescUl is None or len(itmDescUl) == 0:
        return
    contents = itmDescUl[0].contents
    for con in contents:
        if "书名" in con.next:
            book.setName(con.next.replace("书名: ", ""))
        if "ISBN" in con.next:
            book.setIsbn(con.next.replace("ISBN编号: ", ""))
        if ("作者" in con.next) or ("编者" in con.next):
            if "作者地区" not in con.next:
                book.setAuther(con.next.replace("作者: ", ""))
        if ("定价:" in con.next) or ("定价：" in con.next):
            book.setFixPrice(con.next.replace("定价: ", "").replace("价格: ", "").replace("定价：", ""))
        if ("出版社" in con.next) or ("出版社" in con.next):
            book.setPress(con.next.replace("出版社名称:", "").replace(" ", ""))

    ##解析是否有sku 信息

    # 写入数据库
    dataReptiledb.insertDetailPrice(book)
    logUtils.logger.info("线程{threadName} - 基础信息抓取完成 {itemId}- 代理IP:{proxyIp}".format( threadName=threading.current_thread().getName(), itemId=itemId, proxyIp=ip))
    return book,1
def processBookDefaultInfo(category, logUtils,startId,endId):
    pageSize = 10000
    while True:
        errCnt = 0
        retryCnt = 0
        index = 0
        itemUrls = dataReptiledb.getItemUrl(category=category, page_size=pageSize,startId=startId,endId=endId)
        proxyIp = None
        if itemUrls is None or len(itemUrls) <= 0:
            break
        while index <= len(itemUrls) - 1:
            try:
                proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
                #proxyIp = "22925:4355@140.249.194.50:23041"
                processDefaultBookData(itemUrls[index], proxyIp, logUtils)
                dataReptiledb.updateSuccessFlag(flag=1, itemId=itemUrls[index].itemId)
                dataReptiledb.updateBookSuccessFlag(flag=1,itemId=itemUrls[index].itemId)
            except Exception as  e:
                logUtils.logger.error("线程{threadName} - {itemId} 发生异常 - 代理IP:{proxyIp} - {e}".format(
                    threadName=threading.current_thread().getName(), itemId=itemUrls[index].itemId, proxyIp=proxyIp,
                    e=e))
                #重试次数统计
                retryCnt += 1
                if retryCnt >= constants.retry_cnt:
                    index += 1
                    retryCnt = 0
                time.sleep(random.randint(1,3))
                proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
            else:
                index += 1
def processDefaultInfo(categorys,logUtils,threadNum,startId,endId):
    dataReptiledb.init(None, "./logs/db-current.log")
    if categorys is None or len(categorys) <= 0:
        logUtils.logger.error("未找到需要处理的分类")
        return
    threadParamMap = {}

    for index in range(0, threadNum):
        if index < len(categorys):
            threading.Thread(target=processBookDefaultInfo, args=(categorys[index],logUtils,startId,endId),
                             name="$自定义<->" + categorys[index] + "<->"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+"$").start()
            # 每个账号绑定一个分类
            threadParamMap[index] = categorys[index]
        else:
            logUtils.logger.info("线程启动结束")
    return threadParamMap

#nohup python getItemBaseDataCurrent.py   >> logs/nohup-base-current.log 2>&1  &

#nohup python getItemBaseDataCurrent.py -a 500000 -b 600000 >> logs/nohup-base-current1.log 2>&1 &
#nohup python getItemBaseDataCurrent.py -a 600000 -b 700000 >> logs/nohup-base-current2.log 2>&1 &
#nohup python getItemBaseDataCurrent.py -a 700000 -b 800000 >> logs/nohup-base-current3.log 2>&1 &
#nohup python getItemBaseDataCurrent.py -a 800000 -b 900000 >> logs/nohup-base-current4.log 2>&1 &
#nohup python getItemBaseDataCurrent.py -a 900000 -b 1000000 >> logs/nohup-base-current5.log 2>&1 &
#nohup python getItemBaseDataCurrent.py -a 1000000 -b 1100000 >> logs/nohup-base-current6.log 2>&1 &
#nohup python getItemBaseDataCurrent.py -a 1100000 -b 1200000 >> logs/nohup-base-current7.log 2>&1 &
#nohup python getItemBaseDataCurrent.py -a 1200000 -b 1300000 >> logs/nohup-base-current8.log 2>&1 &
if __name__ == '__main__':
    startId = 0
    endId = 999999999
    opts, args = getopt.getopt(sys.argv[1:], "a:b:")
    for opt, arg in opts:
        if opt == "-a":
            startId = arg
        if opt == "-b":
            endId = arg

    logUtils = Logger(filename='./logs/detail-current.log', level='info')
    dataReptiledb.init(None, "./logs/db-current.log")
    # 从item_url 中查
    categorys = dataReptiledb.getNotDealCategoryByItemUrl(startId,endId)
    if categorys is None:
        logUtils.logger.error("未找到需要处理的分类")
    # 开始处理
    processDefaultInfo(categorys=categorys, logUtils=logUtils,threadNum=len(categorys),startId=startId,endId=endId)
    while True:
        try:
            threadParamMap = {}
            time.sleep(60)
            custThreadCnt = 0
            threads = threading.enumerate()
            if threads is None or len(threads) ==0:
                continue
            for thread in threads:
                if "自定义" in thread.name:
                    custThreadCnt += 1
            if custThreadCnt == 0:
                # 排除正在运行的分类
                categorys = dataReptiledb.getNotDealCategoryByItemUrl(startId,endId)
                runCategorys = threadParamMap.values()
                # 得到未执行的分类
                freeCategorys = list(set(categorys).difference(set(runCategorys)))
                processDefaultInfo(categorys=categorys, logUtils=logUtils,threadNum=len(categorys),startId=startId,endId=endId)
        except Exception as e:
            logUtils.logger.error("线程检测出现异常")
            logUtils.logger.error(u"线程检测出现异常", e, exc_info=True, stack_info=True)