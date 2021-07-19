from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
import threading, time
import getIpProxyPool
import constants

dataReptiledb.host = "192.168.47.210"
# 促销 url
promotionUrl = 'https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false&itemId={itemId}&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621928176000&isRegionLevel=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&timestamp=1622029723119&isg=eBIE8Mulj-IREQ65BOfChurza779JIRYjuPzaNbMiOCP_Hf671mVW6sFIY8BCnGVh6AwJ3oiiBs_BeYBq_C-nxvOa6Fy_3Hmn&isg2=BPz8DUnnsCHnEoT3_AthiILwzZqu9aAfdLEeZdZ9POfMoZwr_wX0r_dQgcnZ0th3'


# logUtils = Logger(filename='./logs/current-detail.log', level='info')

# file_object = open('D:\\爬虫\\TM\\item-detail-promo.txt', "a", encoding='utf-8')
# file_object = open('./TM/item-detail-promo-01.txt', "a", encoding='utf-8')


# 干扰函数
def disturbUrl(header, ip, logUtils):
    proxy = {'http:': "http://" + ip, 'https:': "https://" + ip}
    disturb_urls = []
    randint = random.randint(1, 10)
    #随机请求其他请求
    if randint % 2 == 0:
        disturb_urls = dataReptiledb.getRandDisturbUrl()
    if disturb_urls is None or len(disturb_urls) == 0:
        return
    session = HTMLSession()
    try:
        for (key,value) in disturb_urls[0].items():
            if value is not None and len(value) !=0 :
                session.get(url=value, headers=header, proxies=proxy)
                time.sleep(random.randint(1, 3))
                logUtils.logger.info("{thread} 执行一次 其他请求 url:{url} ".format(thread=threading.current_thread().getName(),
                                                                            url=value))
    except Exception as e:
        logUtils.logger.info("线程{thread} 执行其他请求发生异常".format(thread=threading.current_thread().getName()))
        proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
        proxy = {'http:': "http://" + proxyIp, 'https:': "https://" + proxyIp}
        try:
            for (key, value) in disturb_urls[0].items():
                if value is not None and len(value) != 0:
                    session.get(url=value, headers=header, proxies=proxy)
                    time.sleep(random.randint(1, 3))
                    logUtils.logger.info("{thread} 执行一次 其他请求 url:{url} ".format(thread=threading.current_thread().getName(),
                                                                                url=value))
        except:
            pass
    #


def write_db(detailUrl, shopName, category):
    item_urls = []
    for url in detailUrl:
        if url is not None:
            item_id = re.match(".*?(id=.*&).*", url, re.S).group(1).split("&")[0].replace('id=', '')
            item_url = "http:" + url
            itemUrl = ItemUrl(itemId=item_id, itemUrl=item_url, shopName=shopName, category=category)
            item_urls.append(itemUrl)
    dataReptiledb.insertItemUrl(item_urls)


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


# 实际解析进本信息方法
def processDefaultBookData(itemUrlEntity, header, ip, logUtils):
    proxy = {'http:': "http://" + ip, 'https:': "https://" + ip}
    session = HTMLSession()
    detailResponse = session.get(itemUrlEntity.itemUrl, proxies=proxy)
    detailHtmlSoup = BeautifulSoup(detailResponse.text, features='html.parser')
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
            book.setPress(con.next.replace("出版社名称:", ""))

    # 获取促销信息
    # processPromotion(book, header, ipList)
    # disturbUrl(header, ip)
    # 写入数据库
    dataReptiledb.insertDetailPrice(book)
    logUtils.logger.info("线程{threadName} - 基础信息抓取完成 {itemId}- 代理IP:{proxyIp}".format( threadName=threading.current_thread().getName(), itemId=itemId, proxyIp=ip))
    # time.sleep(5)
    # time.sleep(random.randint(2, 10))
    return book,1


# 实际解析促销价方法
def processPromotionBookData(book, header, ip, logUtils):
    threadName = threading.current_thread().getName()
    proxy = {'http:': "http://" + ip, 'https:': "https://" + ip}
    session = HTMLSession()
    promotionJsonp = session.get(promotionUrl.format(itemId=book.getTmId()), headers=header,
                                 proxies=proxy)
    try:
        promotionJSON = loads_jsonp(promotionJsonp.text)
    except Exception as e:
        # cookie 解析失败更新账号
        dataReptiledb.updateHeaderStatus(0, header['account'])
        logUtils.logger.error(
            "线程{threadName} - {itemId} 解析jsonp 失败,cookie 失效,代理IP:{ip}".format(threadName=threadName, itemId=book.getTmId(),ip=ip))
        raise Exception(
            "线程{threadName} - {itemId} 解析jsonp 失败,cookie 失效,代理IP:{ip}".format(threadName=threadName, itemId=book.getTmId(),ip=ip))
    else:
        #商品已经下架，
        if promotionJSON.get("success") is False:
            logUtils.logger.error(
                "线程{threadName} - {itemId} 商品已经下载 ,代理IP:{ip}".format(threadName=threadName, itemId=book.getTmId(),ip=ip))
            dataReptiledb.insertDetailPrice(book)
            #商品已经下架
            return 2
        if promotionJSON.get("defaultModel") is None:
            dataReptiledb.updateHeaderStatus(0, header['account'])
            logUtils.logger.error(
                "线程{threadName} - {itemId} 获取不到促销信息啦，可能cookie失效".format(threadName=threadName, itemId=book.getTmId()))
            # time.sleep(random.randint(2, 10))
            raise Exception(
                "线程{threadName} - {itemId} 获取不到促销信息啦，可能cookie失效".format(threadName=threadName, itemId=book.getTmId()))

    # 如果是店铺vip 登陆状态下，这个价格就是实际的vip价格
    price = promotionJSON['defaultModel']['itemPriceResultDO']['priceInfo'].get('def', {}).get('price', 0)
    # 促销列表
    promotionList = promotionJSON['defaultModel']['itemPriceResultDO']['priceInfo'].get('def', {}).get("promotionList",
                                                                                                       None)
    # 促销金额
    promotionPrice = 0
    promotionPriceType = ''
    if promotionList is None or len(promotionList) == 0:
        promotionPrice = price
        book.setPromotionPrice(promotionPrice)
    else:
        promotionPrice = promotionList[0].get('price', 0)
        promotionPriceType = promotionList[0].get('type', "")
        promotionPriceDesc = promotionList[0].get('promText', "")
        startTime = promotionList[0].get("startTime")
        endTime = promotionList[0].get("endTime")
        # 设置促销价
        book.setPromotionPrice(promotionPrice)
        book.setPromotionType(promotionPriceType)
        book.setPromotionPriceDesc(promotionPriceDesc)
        book.setActiveStartTime(startTime)
        book.setActiveEndTime(endTime)
    # 获取销量
    seles = promotionJSON['defaultModel'].get("sellCountDO", {}).get("sellCount", "0")
    book.setSales(sales=seles)
    # 活动
    tmallShopProm = promotionJSON['defaultModel']['itemPriceResultDO']['tmallShopProm']
    if len(tmallShopProm) != 0:
        promPlanMsg = []
        for shopProm in tmallShopProm:
            promPlanMsg.append(",".join(shopProm['promPlanMsg']))
        book.setActiveDesc(promPlanMsg)
    #
    # 提取相关sku
    # relatedAuctionsDO = promotionJSON.get("defaultModel").get("relatedAuctionsDO")
    # detailUrl = []
    # if relatedAuctionsDO is not None and relatedAuctionsDO.get("relatedAuctions", None) is not None:
    #     # 开始遍历提取
    #     relatedAuctions = relatedAuctionsDO.get("relatedAuctions")
    #     if len(relatedAuctions) > 0:
    #         for related in relatedAuctions:
    #             itemId = related.get("itemId")
    #             url = "//detail.tmall.com/item.htm?id=" + str(itemId) + "&temp=111"
    #             detailUrl.append(url)
    #         write_db(detailUrl, shopName=book.getShopName(), category=book.getCategory())

    # 写入文件
    # file_object.write(book.toString() + "\n")
    # file_object.flush()
    # logUtils.logger.info("线程{threadName} process book {id}".format(threadName=threadName,id=book.tmId))

    # 保存数据
    dataReptiledb.insertDetailPrice(book)
    logUtils.logger.info("线程{threadName} 促销信息抓取完成 {id}".format(threadName=threadName, id=book.tmId))
    return  1


# 多线程调度方法
def processBookInfo(category, header, logUtils):
    pageSize = 10000
    while True:
        errCnt = 0
        retryCnt = 0
        index = 0
        proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
        itemUrls = dataReptiledb.getItemUrl(category=category, page_size=pageSize)
        if itemUrls is None or len(itemUrls) <= 0:
            break
        while index <= len(itemUrls) - 1:
            try:
                book,status = processDefaultBookData(itemUrls[index], header, proxyIp, logUtils)
                dataReptiledb.updateSuccessFlag(flag=1, itemId=itemUrls[index].itemId)
                proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
                #如果status = 2 说明已经下架，
                if status != 2:
                    status = processPromotionBookData(book, header, proxyIp, logUtils)
                    logUtils.logger.info("线程{threadName} - {itemId} 获取书籍信息成功 - 代理IP:{proxyIp}".format(
                            threadName=threading.current_thread().getName(),
                            itemId=itemUrls[index].itemId, proxyIp=proxyIp))
                    time.sleep(random.randint(5, 10))
                    # 执行干扰函数
                disturbUrl(header, proxyIp, logUtils)
            except Exception as  e:
                errCnt+=1
                logUtils.logger.error("线程{threadName} - {itemId} 发生异常 - 代理IP:{proxyIp} - {e}".format(
                    threadName=threading.current_thread().getName(), itemId=itemUrls[index].itemId, proxyIp=proxyIp,
                    e=e))
                #超过阀值，直接退出
                if errCnt > constants.error_cnt:
                    return
                #重试次数统计
                retryCnt += 1
                if retryCnt >= constants.retry_cnt:
                    index += 1
                    retryCnt = 0
                time.sleep(random.randint(10,20))
                proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
                headers = dataReptiledb.getHeaders(header['account'])
                if headers is None or len(headers) == 0:
                    time.sleep(random.randint(10, 20))
                #当前cookie 已经被禁用，直接返回
                elif headers[0].get("status") < 0:
                    return
                else:
                    header = headers[0]
                    header.pop("status")
            else:
                try:
                    dataReptiledb.updateBookSuccessFlag(flag=status, itemId=itemUrls[index].itemId)
                except:
                    logUtils.logger.info("线程{threadName} - {itemId} 更新is_sucess标志失败".format(
                        threadName=threading.current_thread().getName(), itemId=itemUrls[index].itemId))
                else:
                    logUtils.logger.info("线程{threadName} - {itemId} 处理完成,代理IP:{ip}".format(threadName=threading.current_thread().getName(), itemId=itemUrls[index].itemId, ip=proxyIp))
                index += 1
            finally:
                time.sleep(random.randint(1, 10))


# 多线程调度方法
def processBookPromoInfo(category, header, logUtils):
    if header is None:
        return
    while True:
        errCnt = 0
        sucCnt = 0
        retryCnt = 0
        index = 0
        proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
        books = dataReptiledb.getBookByNotHavePromo(category=category, size=1000)
        if books is None or len(books) <= 0:
            break
        while index <= len(books) - 1:
            try:
                if header is None:
                    return
                status = processPromotionBookData(books[index], header, proxyIp, logUtils)
                sucCnt += 1
                time.sleep(random.randint(10, 20))
                # 执行干扰函数
                disturbUrl(header, proxyIp, logUtils)
            except Exception as  e:
                errCnt +=1
                logUtils.logger.info("成功统计-线程{threadName} 本次执行 {sucCnt}成功后 发生异常".format(threadName=threading.current_thread().getName(),sucCnt=sucCnt))
                sucCnt = 0
                logUtils.logger.error(e)
                logUtils.logger.error("线程{threadName} - {itemId} 发生异常".format(threadName=threading.current_thread().getName(), itemId=books[index].tmId))
                #
                if errCnt > constants.error_cnt:
                    return
                proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
                retryCnt += 1
                if retryCnt >= constants.retry_cnt:
                    index += 1
                    retryCnt = 0
                headers = dataReptiledb.getHeaders(header['account'])
                if headers is None or len(headers) == 0:
                    time.sleep(random.randint(10, 20))
                    # 当前cookie 已经被禁用，直接返回
                elif headers[0].get("status") < 0:
                    return
                else:
                    header = headers[0]
                    header.pop("status")
                time.sleep(random.randint(10, 20))
            else:
                try:
                    dataReptiledb.updateBookSuccessFlag(flag=status, itemId=books[index].tmId)
                except:
                    logUtils.logger.info("线程{threadName} - {itemId} 更新is_sucess标志失败".format(threadName=threading.current_thread().getName(), itemId=books[index].tmId))
                else:
                    logUtils.logger.info("线程{threadName} - {itemId} 处理完成,代理IP:{ip}".format(threadName=threading.current_thread().getName(), itemId=books[index].tmId,ip=proxyIp))
                index += 1
            finally:
                time.sleep(random.randint(3, 10))


def processBookPromoInfoTest(category, headerIndex):
    while True:
        time.sleep(2)
        print(category, headerIndex)


if __name__ == '__main__':
    # region Description
    # try:
    #     i = 1 / 0
    # except Exception as e:
    #     print("%s 处理成功 %s", "AA", e)

    # disturb_urls = dataReptiledb.getRandDisturbUrl()
    # print(disturb_urls)

    # endregion
    # logUtils.logger.info("%s 处理成功 %s", "AA", "AAA")
    dict_test={"k":"1","s":1}
    print(dict_test.pop("k"))