import json
import re
import threading
import time

from bs4 import BeautifulSoup
from requests_html import HTMLSession

import dataReptiledb
import getIpProxyPool
from entity import Book, Logger, SkuInfo,ItemUrl


def macth_brackets(text):
    match = re.search("TShop\\.Setup\\((.*)\\);", text, re.S)
    text = match.group(0)
    stack = []
    match_s = "("
    match_e = ")"
    jsonStr = ""
    start_index = text.find("TShop.Setup") + len("TShop.Setup")
    end_index = len(text) - 1
    for i in range(start_index, end_index):
        if text[i] == match_s:
            stack.append(i)
        if text[i] == match_e:
            stack.pop()
        if len(stack) == 0:
            jsonStr = text[start_index + 1:i]
            break
    return jsonStr


def analySkuInfoJson(jsonStr):
    sku_infos = []
    skuInfoJson = json.loads(jsonStr)
    valItemInfo = skuInfoJson.get("valItemInfo")
    if valItemInfo is None:
        return
    skuList = valItemInfo.get("skuList")
    skuMap = valItemInfo.get("skuMap")
    for jsonSkuInfo in skuList:
        info = SkuInfo(sku_id=None, spu_id=None, name=None, price=None)
        names = jsonSkuInfo.get("names")
        pvs = jsonSkuInfo.get("pvs")
        skuId = jsonSkuInfo.get("skuId")
        price = skuMap.get(";" + pvs + ";").get("price")
        info.sku_id = skuId
        info.name = names
        info.price = price
        sku_infos.append(info)
    return sku_infos


def processDefaultBookData(itemUrlEntity, ip, logUtils):
    proxy = {'http': "http://" + ip, 'https': "https://" + ip}
    session = HTMLSession()
    detailResponse = session.get(itemUrlEntity.itemUrl, proxies=proxy, timeout=(3, 4))
    #detailResponse = session.get(itemUrlEntity.itemUrl)
    detailHtmlSoup = BeautifulSoup(detailResponse.text.encode("utf-8"), features='html.parser')
    book = Book(tmId=itemUrlEntity.itemId, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                promotionPriceDesc=None, price=None, promotionType=None, activeStartTime=None,
                activeEndTime=None,
                activeDesc="", shopName=itemUrlEntity.shopName, category=itemUrlEntity.category, sales="0", press=None,
                skuId=None, skuName=None)
    if "很抱歉，您查看的商品找不到了" in detailResponse.text:
        dataReptiledb.insertDetailPrice(book)
        logUtils.logger.error(
            "线程{threadName} - 商品已经下架 {id}".format(threadName=threading.current_thread().getName(),
                                                  id=itemUrlEntity.itemId))
        return None, 2

    defaultPrice = re.match(".*?(\"defaultItemPrice\":.*&).*", detailResponse.text, re.S).group(1).split(',')[
        0].replace("defaultItemPrice", "").replace('\"', "").replace(":", "").replace(",", "")

    book.setPrice(defaultPrice)
    itmDescUl = detailHtmlSoup.find_all(name="ul", attrs={"id": "J_AttrUL"})
    logUtils.logger.info("{itemId} {itmDescUl}".format(itemId=itemUrlEntity.itemId, itmDescUl=itmDescUl))
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

    ##解析是否有sku信息
    jsonStr = macth_brackets(detailResponse.text)
    sku_infos = analySkuInfoJson(jsonStr)
    logUtils.logger.info("{threadName} <-> {item_id} 下的sku有 {num} 个".format(threadName=threading.current_thread().getName(),item_id=itemUrlEntity.itemId, num= 0 if sku_infos is None else len(sku_infos)))
    if sku_infos is not None and len(sku_infos) > 1:
        for sku_info in sku_infos:
            book.setSkuId(sku_info.sku_id)
            book.setSkuName(sku_info.name)
            book.setFixPrice(sku_info.price)
            dataReptiledb.insertDetailPrice(book)
    else:
        # 写入数据库
        dataReptiledb.insertDetailPrice(book)
    logUtils.logger.info(
        "线程{threadName} - 基础信息抓取完成 {itemId}- 代理IP:{proxyIp}".format(threadName=threading.current_thread().getName(),
                                                                    itemId=itemUrlEntity.itemId, proxyIp=ip))

def split_list(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]


def processBookDataCurrent(itemIds, logUtils):
    for itemId in itemIds:
        proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
        itemUrlEntitys = dataReptiledb.getItemUrlByItemId(itemId=itemId)
        if itemUrlEntitys is None or len(itemUrlEntitys) == 0:
            continue
        itemUrlEntity = itemUrlEntitys[0]
        try:
            processDefaultBookData(itemUrlEntity, proxyIp, logUtils)
        except Exception as  e:
            logUtils.logger.error("线程{threadName} - {itemId} 发生异常 - 代理IP:{proxyIp} - {e}".format(
                threadName=threading.current_thread().getName(), itemId=itemUrlEntity.itemId, proxyIp=proxyIp,
                e=e))
        else:
            logUtils.logger.error("线程{threadName} - {itemId} 基础信息抓取完成 - 代理IP:{proxyIp}".format(
                threadName=threading.current_thread().getName(), itemId=itemUrlEntity.itemId, proxyIp=proxyIp))
            dataReptiledb.updateSuccessFlag(flag=1, itemId=itemUrlEntity.itemId)
            dataReptiledb.updateBookSuccessFlag(flag=1, itemId=itemUrlEntity.itemId)


def executeDefaultBookDataCurrent():
    logUtils = Logger(filename='./logs/detail-base-data.log', level='info')
    dataReptiledb.init(None, "./logs/db-current.log")
    size = 20000
    n = 1000
    item_ids = dataReptiledb.getNotDealItemUrl(size)
    temp_ids = split_list(item_ids, n)
    threadIndex = 0
    for tmp in temp_ids:
        threading.Thread(target=processBookDataCurrent, args=(tmp, logUtils),
                         name="$自定义"+ str(threadIndex) +"<-> "+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "$").start()
        threadIndex+=1

if __name__ == '__main__':
    logUtils = Logger(filename='./logs/detail-current.log', level='info')
    url = ItemUrl(shopName="文轩", itemId="578992496018", itemUrl="https://detail.tmall.com/item.htm?id=578992496018",
                  category="无")
    proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
    processDefaultBookData(url, proxyIp, logUtils)
#
    # match = re.match(".*?(id=\d*)", "https://detail.tmall.com/item.htm?id=41903097818&skuId=1111", re.S).group(1).replace("id=","")
    # print(match)
#nohup python getItemBaseDataCurrent_V2.py  >> logs/nohup-base.log 2>&1 &
# if __name__ == '__main__':
#     # startId = 0
#     # endId = 999999999
#     # opts, args = getopt.getopt(sys.argv[1:], "a:b:")
#     # for opt, arg in opts:
#     #     if opt == "-a":
#     #         startId = arg
#     #     if opt == "-b":
#     #         endId = arg
#
#     logUtils = Logger(filename='./logs/detail-base-data.log', level='info')
#     dataReptiledb.init(None, "./logs/db-current.log")
#     # 从item_url 中查
#     # 开始处理
#     executeDefaultBookDataCurrent()
#     while True:
#         try:
#             threadParamMap = {}
#             time.sleep(120)
#             custThreadCnt = 0
#             threads = threading.enumerate()
#             if threads is None or len(threads) ==0:
#                 continue
#             for thread in threads:
#                 if "自定义" in thread.name:
#                     custThreadCnt += 1
#             if custThreadCnt == 0:
#                 executeDefaultBookDataCurrent()
#         except Exception as e:
#             logUtils.logger.error("线程检测出现异常")
#             logUtils.logger.error(u"线程检测出现异常", e, exc_info=True, stack_info=True)
