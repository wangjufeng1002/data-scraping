from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
import threading, time
import getIpProxyPool

# 干扰 url ,
url = [
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.7.5af911d93V6rF1&ie=utf8&initiative_id=staobaoz_20210219&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E6%AF%8D%E5%A9%B4&suggest=history_1&_input_charset=utf-8&wq=%E6%AF%8D%E5%A9%B4&suggest_query=%E6%AF%8D%E5%A9%B4&source=suggest"
    "https://detail.tmall.hk/hk/item.htm?tbpm=1&spm=a230r.1.14.13.6ebb4793sgX8vA&id=599058260846&cm_id=140105335569ed55e27b&abbucket=17",
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.27.5af911d93V6rF1&q=%E5%AE%B6%E9%A5%B0",
    "https://detail.tmall.com/item.htm?spm=a230r.1.14.23.2bdd38bdRsTfHM&id=37236152544&ns=1&abbucket=17",
    "https://detail.tmall.com/item.htm?spm=a230r.1.14.66.21d3310cNOJUQi&id=625910266423&ns=1&abbucket=17&sku_properties=21735:44500;122276380:44500;161712509:100189285"
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.9.5af911d98mAeHv&q=%E7%8E%A9%E5%85%B7",
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.22.5af911d98mAeHv&q=%E8%8C%B6%E9%85%92",
    "https://huodong.taobao.com/wow/pm/default/pcgroup/c51a5b?spm=a21bo.21814703.201867-main.34.5af911d98mAeHv&disableNav=YES",
    "https://zc-paimai.taobao.com/list/0___%C9%C2%CE%F7____56968001.htm?spm=a2129.22722945.puimod-zc-focus-2016_3973807750.22.ac263b375GRqhd&auction_source=0&st_param=-1&auction_start_seg=-1",
    "https://item.taobao.com/item.htm?spm=a230r.1.14.103.3afd7408nYsLtv&id=541989840451&ns=1&abbucket=17#detail",
    "https://s.taobao.com/search?q=%E7%83%A4%E7%AE%B1&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.21814703.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306",
    "https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w15914280-18716446969.2.3ec85f3bDI42Bi&id=639769508905&scene=taobao_shop&sku_properties=10004:7195672376",
    "https://item.taobao.com/item.htm?spm=a211oj.20087502.2458555970.ditem1.161f2a7bvMjm5c&id=639750024278&utparam=null",
    "https://detail.tmall.com/item.htm?id=644956601075&ali_refid=a3_430583_1006:1123397704:N:y3PNKr3XJ12utMymM/mooQ==:8be43003608f1b0d5114253118183bcf&ali_trackid=1_8be43003608f1b0d5114253118183bcf&spm=a230r.1.14.1&sku_properties=10004:7195672376;5919063:6536025",
    "https://detail.tmall.com/item.htm?spm=a230r.1.14.8.5eee6fbeW1QJix&id=617932940345&cm_id=140105335569ed55e27b&abbucket=18&sku_properties=5919063:6536025",
    "https://chaoshi.detail.tmall.com/item.htm?spm=a230r.1.14.46.5eee6fbeW1QJix&id=632506861144&ns=1&abbucket=18&sku_properties=5919063:6536025;122216431:27772",
    "https://detail.tmall.com/item.htm?spm=a230r.1.14.77.5eee6fbeW1QJix&id=632454557541&ns=1&abbucket=18&sku_properties=5919063:6536025",
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.17.5af911d9hgOf6o&q=%E5%8A%9E%E5%85%AC",
    "https://detail.tmall.com/item.htm?spm=a230r.1.14.20.768e1aefoyLEp6&id=571102285943&ns=1&abbucket=18",
    "https://detail.tmall.com/item.htm?spm=a230r.1.14.46.768e1aefoyLEp6&id=629901738583&ns=1&abbucket=18",
    "https://s.taobao.com/search?spm=a21bo.21814703.201867-main.10.5af911d9hgOf6o&q=%E7%94%B7%E8%A3%85",
    "https://detail.tmall.com/item.htm?spm=a230r.1.14.6.5343442buCOyAA&id=623503217270&cm_id=140105335569ed55e27b&abbucket=18"
]

dataReptiledb.host = "192.168.47.210"
# 促销 url
promotionUrl = 'https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false&itemId={itemId}&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621928176000&isRegionLevel=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&timestamp=1622029723119&isg=eBIE8Mulj-IREQ65BOfChurza779JIRYjuPzaNbMiOCP_Hf671mVW6sFIY8BCnGVh6AwJ3oiiBs_BeYBq_C-nxvOa6Fy_3Hmn&isg2=BPz8DUnnsCHnEoT3_AthiILwzZqu9aAfdLEeZdZ9POfMoZwr_wX0r_dQgcnZ0th3'


# logUtils = Logger(filename='./logs/current-detail.log', level='info')

# file_object = open('D:\\爬虫\\TM\\item-detail-promo.txt', "a", encoding='utf-8')
# file_object = open('./TM/item-detail-promo-01.txt', "a", encoding='utf-8')


# 干扰函数
def disturbUrl(header, ip, logUtils):
    proxy = {'http:': "http://" + ip, 'https:': "https://" + ip}
    time.sleep(random.randint(1, 5))
    randint = random.randint(1, 3)
    if randint % 2 == 0:
        session = HTMLSession()
        try:
            session.get(url=random.choice(url), headers=header,
                        proxies=proxy)
        except:
            proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
            proxy = {'http:': "http://" + proxyIp, 'https:': "https://" + proxyIp}
            session.get(url=random.choice(url), headers=header,
                        proxies=proxy)
            pass
        logUtils.logger.info("{thread} 执行一次 其他请求 ".format(thread=threading.current_thread().getName()))


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
    itemId = re.match(".*?(id=.*&).*", itemUrlEntity.itemUrl, re.S).group(1).split('&')[0].replace('id=', '')
    defaultPrice = re.match(".*?(\"defaultItemPrice\":.*&).*", detailResponse.text, re.S).group(1).split(',')[
        0].replace("defaultItemPrice", "").replace('\"', "").replace(":", "").replace(",", "")

    itmDescUl = detailHtmlSoup.find_all(name="ul", attrs={"id": "J_AttrUL"})
    if itmDescUl is None or len(itmDescUl) == 0:
        return
    book = Book(tmId=itemId, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                promotionPriceDesc=None, price=defaultPrice, promotionType=None, activeStartTime=None,
                activeEndTime=None,
                activeDesc="", shopName=itemUrlEntity.shopName, category=itemUrlEntity.category, sales="0", press=None)
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
            print(con.next.replace("定价: ", "").replace("价格: ", "").replace("定价：", ""))
        if ("出版社" in con.next) or ("出版社" in con.next):
            book.setPress(con.next.replace("出版社名称:", ""))

    # 获取促销信息
    # processPromotion(book, header, ipList)
    # disturbUrl(header, ip)
    # 写入数据库
    dataReptiledb.insertDetailPrice(book)
    logUtils.logger.info(
        "线程{threadName} - process book {id}".format(threadName=threading.current_thread().getName(), id=itemId))
    # time.sleep(5)
    # time.sleep(random.randint(2, 10))
    return book


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
            "线程{threadName} - {itemId} 解析jsonp 失败，cookie 失效".format(threadName=threadName, itemId=book.getTmId()))
        raise Exception(
            "线程{threadName} - {itemId} 解析jsonp 失败，cookie 失效".format(threadName=threadName, itemId=book.getTmId()))
    else:
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
    relatedAuctionsDO = promotionJSON.get("defaultModel").get("relatedAuctionsDO")
    detailUrl = []
    if relatedAuctionsDO is not None and relatedAuctionsDO.get("relatedAuctions", None) is not None:
        # 开始遍历提取
        relatedAuctions = relatedAuctionsDO.get("relatedAuctions")
        if len(relatedAuctions) > 0:
            for related in relatedAuctions:
                itemId = related.get("itemId")
                url = "//detail.tmall.com/item.htm?id=" + str(itemId) + "&temp=111"
                detailUrl.append(url)
            write_db(detailUrl, shopName=book.getShopName(), category=book.getCategory())

    # 写入文件
    # file_object.write(book.toString() + "\n")
    # file_object.flush()
    # logUtils.logger.info("线程{threadName} process book {id}".format(threadName=threadName,id=book.tmId))

    # 保存数据
    dataReptiledb.insertDetailPrice(book)
    logUtils.logger.info("线程{threadName} process book {id}".format(threadName=threadName, id=book.tmId))


# 多线程调度方法
def processBookInfo(category, header, logUtils):
    pageSize = 10000
    while True:
        retryCnt = 0
        index = 0
        proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
        itemUrls = dataReptiledb.getItemUrl(category=category, page_size=pageSize)
        if itemUrls is None or len(itemUrls) <= 0:
            break
        while index <= len(itemUrls) - 1:
            try:
                book = processDefaultBookData(itemUrls[index], header, proxyIp, logUtils)
                proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
                processPromotionBookData(book, header, proxyIp, logUtils)
                index += 1
                logUtils.logger.error(
                    "线程{threadName} - {itemId} 获取书籍信息成功 - 代理IP:{proxyIp}".format(
                        threadName=threading.current_thread().getName(),
                        itemId=itemUrls[index].itemId), proxyIp=proxyIp)
                time.sleep(random.randint(1, 5))
            except Exception as  e:
                logUtils.logger.error("线程{threadName} - {itemId} 发生异常 - 代理IP:{proxyIp} - {e}".format(
                    threadName=threading.current_thread().getName(), itemId=itemUrls[index].itemId, proxyIp=proxyIp,
                    e=e))
                proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
                retryCnt += 1
                if retryCnt >= 20:
                    index += 1
                    retryCnt = 0
            else:
                dataReptiledb.updateSuccessFlag(1, itemId=itemUrls[index].itemId)
            finally:
                time.sleep(random.randint(1, 10))


# 多线程调度方法
def processBookPromoInfo(category, header, logUtils):
    if header is None:
        return
    while True:
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
                processPromotionBookData(books[index], header, proxyIp, logUtils)
                sucCnt += 1
                time.sleep(random.randint(10, 20))
                # 执行干扰函数
                disturbUrl(header, proxyIp, logUtils)
            except Exception as  e:
                logUtils.logger.info(
                    "成功统计-线程{threadName} 本次执行 {sucCnt}成功后 发生异常".format(threadName=threading.current_thread().getName(),
                                                                       sucCnt=sucCnt))
                sucCnt = 0
                logUtils.logger.error(e)
                logUtils.logger.error(
                    "线程{threadName} - {itemId} 发生异常".format(threadName=threading.current_thread().getName(),
                                                            itemId=books[index].tmId))
                proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
                retryCnt += 1
                if retryCnt >= 20:
                    index += 1
                    retryCnt = 0
                headers = dataReptiledb.getHeaders(header['account'])
                if headers is None or len(headers) == 0:
                    time.sleep(random.randint(10, 20))
                else:
                    header = headers[0]
                time.sleep(random.randint(10, 20))
            else:
                try:
                    dataReptiledb.updateBookSuccessFlag(flag=1, itemId=books[index].tmId)
                except:
                    logUtils.logger.info("线程{threadName} - {itemId} 更新is_sucess标志失败".format(
                        threadName=threading.current_thread().getName(), itemId=books[index].tmId))
                else:
                    logUtils.logger.info(
                        "线程{threadName} - {itemId} 处理完成".format(threadName=threading.current_thread().getName(),
                                                                itemId=books[index].tmId))
                index += 1
            finally:
                time.sleep(random.randint(3, 10))


def processBookPromoInfoTest(category, headerIndex):
    while True:
        time.sleep(2)
        print(category, headerIndex)


if __name__ == '__main__':
    # region Description
    try:
        i = 1 / 0
    except Exception as e:
        print("%s 处理成功 %s", "AA", e)
    # endregion
    # logUtils.logger.info("%s 处理成功 %s", "AA", "AAA")
