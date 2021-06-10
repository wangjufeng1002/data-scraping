from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl,Logger
import threading, time
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

dataReptiledb.host="127.0.0.1"
# 促销 url
# promotionUrl = 'https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false' \
#                '&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false' \
#                '&itemId={itemId}&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621464441000&isRegionLevel' \
#                '=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&casynSearchallback' \
#                '=setMdskip&timestamp=1621491544699&isg=eBIE8Mulj-IREMTiBOfZhurza779OIRAguPzaNbMiOCPOefe' \
#                '--xPW6s7QLTwCnGVh6YBJ3oiiBs_BeYBqgI-nxvOa6Fy_LDmn&isg2=BDo6VN' \
#                '-xDhCfh4L9DsXP4jDGi2Bc677FZkeY70QzxU2DN9pxLXuv1QAGh8PrpzZd&ref=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm' \
#                '%3Da1z10.3-b-s.w4011-23389038992.173.483f765292VfDy%26id%3D555824274521%26rn' \
#                '%3D596ce34d3b21d41a4baf27d1cfaf0828%26abbucket%3D16'
promotionUrl = 'https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false&itemId={itemId}&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621928176000&isRegionLevel=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&timestamp=1622029723119&isg=eBIE8Mulj-IREQ65BOfChurza779JIRYjuPzaNbMiOCP_Hf671mVW6sFIY8BCnGVh6AwJ3oiiBs_BeYBq_C-nxvOa6Fy_3Hmn&isg2=BPz8DUnnsCHnEoT3_AthiILwzZqu9aAfdLEeZdZ9POfMoZwr_wX0r_dQgcnZ0th3'

logUtils = Logger(filename='./logs/wenxuan-detail.log', level='info')
# 干扰函数
def disturbUrl(header, ip):
    time.sleep(random.randint(1, 5))
    randint = random.randint(1, 3)
    if randint % 2 == 0:
        session = HTMLSession()
        session.get(url=random.choice(url), headers=header,
                    proxies={'http': ip})
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


def processPriceData(itemUrlEntity, header, ipList):
    session = HTMLSession()
    detailResponse = session.get(itemUrlEntity.itemUrl, headers=header, proxies={'http://': random.choice(ipList)})
    detailHtmlSoup = BeautifulSoup(detailResponse.text, features='html.parser')
    itemId = re.match(".*?(id=.*&).*", itemUrlEntity.itemUrl, re.S).group(1).split('&')[0].replace('id=', '')
    itmDescUl = detailHtmlSoup.find_all(name="ul", attrs={"id": "J_AttrUL"})
    if itmDescUl is None or len(itmDescUl) == 0:
        return
    book = Book(tmId=itemId, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                promotionPriceDesc=None, price=None, promotionType=None, activeStartTime=None, activeEndTime=None,
                activeDesc="", shopName=itemUrlEntity.shopName, category=itemUrlEntity.category)
    contents = itmDescUl[0].contents
    for con in contents:
        if "书名" in con.next:
            book.setName(con.next.replace("书名: ", ""))
        if "ISBN" in con.next:
            book.setIsbn(con.next.replace("ISBN编号: ", ""))
        if ("作者" in con.next) or ("编者" in con.next):
            if "作者地区" not in con.next:
                book.setAuther(con.next.replace("作者: ", ""))
        if ("定价" in con.next) or ("价格" in con.next):
            book.setFixPrice(con.next.replace("定价: ", "").replace("价格: ", ""))

    ip = random.choice(ipList)
    promotionJsonp = session.get(promotionUrl.format(itemId=itemId), headers=header,
                                 proxies={'http://': random.choice(ipList)})

    promotionJSON = loads_jsonp(promotionJsonp.text)
    if promotionJSON.get("defaultModel") is None:
        print("{itemId} 获取不到促销信息啦，可能cookie失效".format(itemId=itemId))
        time.sleep(random.randint(2, 10))
        return

    price = promotionJSON['defaultModel']['itemPriceResultDO']['priceInfo'].get('def', {}).get('price')
    # 设置默认价格
    book.setPrice(price)
    # 促销列表
    promotionList = promotionJSON['defaultModel']['itemPriceResultDO']['priceInfo'].get('def', {}).get("promotionList",
                                                                                                       None)
    # 促销金额
    promotionPrice = 0
    promotionPriceType = ''
    if promotionList is None or len(promotionList) == 0:
        promotionPrice = 0
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

    # book.setPromotionPriceDesc(promotionPriceDesc)
    # 活动
    tmallShopProm = promotionJSON['defaultModel']['itemPriceResultDO']['tmallShopProm']
    if len(tmallShopProm) != 0:
        promPlanMsg = []
        for shopProm in tmallShopProm:
            promPlanMsg.append(",".join(shopProm['promPlanMsg']))
        book.setActiveDesc(promPlanMsg)
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
            write_db(detailUrl, shopName=itemUrlEntity.shopName, category=itemUrlEntity.category)
        # 执行干扰函数
    disturbUrl(header, ip)
    # 写入数据库
    dataReptiledb.insertDetailPrice(book)
    # file_result.write(book.toString() + '\n')
    # file_result.flush()
    print("process {id}".format(id=itemId))
    time.sleep(random.randint(2, 10))
    # time.sleep(random.randint(10, 20))





def getUrlDetailUrlFromDB(category):
    # headers 游标
    headersIndex = 0
    # 获取数据库中的 headers
    headers = dataReptiledb.getHeaders()
    # 获取代理ip
    ipList = dataReptiledb.getIpList()
    # 获取url
    page = 1
    pageSize = 1000
    errorCnt = 0
    while True:
        print("处理第%d页数据" % page)
        item_urls = dataReptiledb.getItemUrl(category, page, pageSize)
        if item_urls is None:
            break
        else:
            i = 0
            while i <= len(item_urls) - 1:
                url = item_urls[i]
                if url is None:
                    continue
                try:
                    processPriceData(url, headers[headersIndex], ipList=ipList)
                    i += 1
                except Exception as e:
                    errorCnt += 1
                    print("发生了点异常", e)
                    if headersIndex == len(headers) - 1:
                        headers = dataReptiledb.getHeaders()
                        headersIndex = 0
                    else:
                        headersIndex += 1
                    if errorCnt >= 20:
                        errorCnt = 0
                        i += 1
                        dataReptiledb.updateSuccessFlag(2, url.itemId)
                    time.sleep(random.randint(1, 20))
                else:
                    dataReptiledb.updateSuccessFlag(1, url.itemId)
        page += 1


if __name__ == '__main__':
    print("start")
    threading.Thread(target=getUrlDetailUrlFromDB, args=('xs',), name="xs").start()
    threading.Thread(target=getUrlDetailUrlFromDB, args=('sh_2',), name="sh_2").start()
    threading.Thread(target=getUrlDetailUrlFromDB, args=('sh_1',), name="sh_1").start()
    threading.Thread(target=getUrlDetailUrlFromDB, args=('qc',), name="qc").start()
    threading.Thread(target=getUrlDetailUrlFromDB, args=('wx',), name="wx").start()
    threading.Thread(target=getUrlDetailUrlFromDB, args=('jf',), name="jf").start()
    threading.Thread(target=getUrlDetailUrlFromDB, args=('ts',), name="ts").start()
    threading.Thread(target=getUrlDetailUrlFromDB, args=('cglz',), name="cglz").start()
    threading.Thread(target=getUrlDetailUrlFromDB, args=('kj',), name="kj").start()
