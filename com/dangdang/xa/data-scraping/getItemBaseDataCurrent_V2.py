import json
import re
import threading
import time

from bs4 import BeautifulSoup
from requests_html import HTMLSession

import dataReptiledb
import getIpProxyPool
from entity import Book, Logger, SkuInfo, ItemUrl


def get_proxy_ip(type):
    proxyIp = None
    if type == 1:
        return getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
    if type == 2:
        while True:
            session = HTMLSession()
            response = session.get(
                "http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=11&pack=181521&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4")
            proxyIp = response.text.replace("\r","").replace("\n","")
            if "code" in proxyIp:
                time.sleep(3)
            else:
                return proxyIp



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
def macth_h5_detail(text):
    match = re.search("_DATA_Detail =(.*)};", text, re.S)
    text = match.group(0)
    stack = []
    match_s = "{"
    match_e = "}"
    jsonStr = ""
    start_index = text.find("_DATA_Detail =") + len("_DATA_Detail =")
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
    headers = dataReptiledb.getUseHeaders(None)
    detailResponse = session.get(itemUrlEntity.itemUrl, proxies=proxy,headers=headers[0], timeout=(3, 4))
    #detailResponse = session.get(itemUrlEntity.itemUrl)
    # detailResponse = session.get(itemUrlEntity.itemUrl)
    detailHtmlSoup = BeautifulSoup(detailResponse.text.encode("utf-8"), features='html.parser')
    book = Book(tmId=itemUrlEntity.itemId, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                promotionPriceDesc=None, price=None, promotionType=None, activeStartTime=None,
                activeEndTime=None,
                activeDesc="", shopName=itemUrlEntity.shopName, category=itemUrlEntity.category, sales="0", press=None,
                skuId=None, skuName=None)
    if "??????????????????????????????????????????" in detailResponse.text:
        dataReptiledb.insertDetailPrice(book)
        logUtils.logger.error(
            "??????{threadName} - ?????????????????? {id}".format(threadName=threading.current_thread().getName(),
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
        if "??????" in con.next:
            book.setName(con.next.replace("??????:??", ""))
        if "ISBN" in con.next:
            book.setIsbn(con.next.replace("ISBN??????:??", ""))
        if ("??????" in con.next) or ("??????" in con.next):
            if "????????????" not in con.next:
                book.setAuther(con.next.replace("??????:??", ""))
        if ("??????:" in con.next) or ("?????????" in con.next):
            book.setFixPrice(con.next.replace("??????:??", "").replace("??????:??", "").replace("?????????", ""))
        if ("?????????" in con.next) or ("?????????" in con.next):
            book.setPress(con.next.replace("???????????????:", "").replace("??", ""))

    ##???????????????sku??????
    jsonStr = macth_brackets(detailResponse.text)
    sku_infos = analySkuInfoJson(jsonStr)
    logUtils.logger.info(
        "{threadName} <-> {item_id} ??????sku??? {num} ???".format(threadName=threading.current_thread().getName(),
                                                           item_id=itemUrlEntity.itemId,
                                                           num=0 if sku_infos is None else len(sku_infos)))
    if sku_infos is not None and len(sku_infos) > 1:
        for sku_info in sku_infos:
            book.setSkuId(sku_info.sku_id)
            book.setSkuName(sku_info.name)
            book.setFixPrice(sku_info.price)
            dataReptiledb.insertDetailPrice(book)
    else:
        # ???????????????
        dataReptiledb.insertDetailPrice(book)
    logUtils.logger.info(
        "??????{threadName} - ???????????????????????? {itemId}- ??????IP:{proxyIp}".format(threadName=threading.current_thread().getName(),
                                                                    itemId=itemUrlEntity.itemId, proxyIp=ip))


def split_list(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]


def processBookDataCurrent(itemIds, logUtils):
    proxyIp = get_proxy_ip(1)
    logUtils.logger.info("getIpProxyPool ????????????IP proxyIp:{proxyIp}".format(proxyIp=proxyIp))
    for itemId in itemIds:
        itemUrlEntitys = dataReptiledb.getItemUrlByItemId(itemId=itemId)
        if itemUrlEntitys is None or len(itemUrlEntitys) == 0:
            continue
        itemUrlEntity = itemUrlEntitys[0]
        try:
            processDefaultBookData(itemUrlEntity, proxyIp, logUtils)
        except Exception as  e:
            logUtils.logger.error("??????{threadName} - {itemId} ???????????? - ??????IP:{proxyIp} - {e}".format(
                threadName=threading.current_thread().getName(), itemId=itemUrlEntity.itemId, proxyIp=proxyIp,
                e=e))
            proxyIp = get_proxy_ip(1)
            logUtils.logger.info("getIpProxyPool ????????????IP proxyIp:{proxyIp}".format(proxyIp=proxyIp))
        else:
            logUtils.logger.info("??????{threadName} - {itemId} ???????????????????????? - ??????IP:{proxyIp}".format(
                threadName=threading.current_thread().getName(), itemId=itemUrlEntity.itemId, proxyIp=proxyIp))
            dataReptiledb.updateSuccessFlag(flag=1, itemId=itemUrlEntity.itemId)
            dataReptiledb.updateBookSuccessFlag(flag=1, itemId=itemUrlEntity.itemId)


def executeDefaultBookDataCurrent():
    logUtils = Logger(filename='./logs/detail-base-data.log', level='info')
    dataReptiledb.init(None, "./logs/db-current.log")
    size = 1000
    n = 1000
    item_ids = dataReptiledb.getNotDealItemUrl(size)
    temp_ids = split_list(item_ids, n)
    threadIndex = 0
    for tmp in temp_ids:
        threading.Thread(target=processBookDataCurrent, args=(tmp, logUtils),
                         name="$?????????" + str(threadIndex) + "<-> " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                 time.localtime()) + "$").start()
        threadIndex += 1


# if __name__ == '__main__':
#     logUtils = Logger(filename='./logs/detail-current.log', level='info')
#     url = ItemUrl(shopName="??????", itemId="578992496018", itemUrl="https://detail.tmall.com/item.htm?id=578992496018",
#                   category="???")
#     proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
#     processDefaultBookData(url, proxyIp, logUtils)
#
# match = re.match(".*?(id=\d*)", "https://detail.tmall.com/item.htm?id=41903097818&skuId=1111", re.S).group(1).replace("id=","")
# print(match)
# nohup python getItemBaseDataCurrent_V2.py  >> logs/nohup-base.log 2>&1 &
if __name__ == '__main__':
    # startId = 0
    # endId = 999999999
    # opts, args = getopt.getopt(sys.argv[1:], "a:b:")
    # for opt, arg in opts:
    #     if opt == "-a":
    #         startId = arg
    #     if opt == "-b":
    #         endId = arg

    logUtils = Logger(filename='./logs/detail-base-data.log', level='info')
    dataReptiledb.init(None, "./logs/db-current.log")
    # ???item_url ??????
    # ????????????
    executeDefaultBookDataCurrent()
    while True:
        try:
            threadParamMap = {}
            time.sleep(120)
            custThreadCnt = 0
            threads = threading.enumerate()
            if threads is None or len(threads) == 0:
                continue
            for thread in threads:
                if "?????????" in thread.name:
                    custThreadCnt += 1
            if custThreadCnt == 0:
                executeDefaultBookDataCurrent()
        except Exception as e:
            logUtils.logger.error("????????????????????????")
            logUtils.logger.error(u"????????????????????????", e, exc_info=True, stack_info=True)
