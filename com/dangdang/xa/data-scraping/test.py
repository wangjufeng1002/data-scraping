from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger,SkuInfo
import threading, time
import getIpProxyPool
from app import entity
import datetime
from slimit.parser import Parser as JavascriptParser
from slimit.visitors import nodevisitor






# if __name__ == '__main__':
# needProcessIndexs=[8001,100201,105301,148101,155301]
# needProcessIndex=8001
# file_object = open('D:\\爬虫\\TM\\remote\\TM\\item-detail-base-bowen.txt', "r", encoding='utf-8')
# file_write = open('D:\\爬虫\\TM\\remote\\TM\\item-detail-base-bowen-x.txt', "a", encoding='utf-8')
#
# lines = file_object.readlines()
# index = 0
# for lin in lines[155300:155400]:
#     file_write.write(lin)
#     file_write.flush()

#
# file_object = open('D:\\爬虫\\TM\\remote\\TM\\1\\item-detail-base.txt', "r", encoding='utf-8')
# file_write = open('D:\\爬虫\\TM\\remote\\TM\\1\\item-detail-base-x.txt', "a", encoding='utf-8')
# lines = file_object.readlines()
# itemIds=set()
# for lin in lines:
#     id = lin.split("\t")[0]
#     if id in itemIds:
#         print("重复")
#     else:
#         itemIds.add(id)
#         file_write.write(lin)
#         file_write.flush()

# file_object = open('D:\\爬虫\\TM\\remote\\TM\\1\\item-detail-base-x.txt', "r", encoding='utf-8')
# file_object = open('D:\\爬虫\\TM\\remote\\TM\\1\\item-detail-base-error.txt', "r", encoding='utf-8')
# lines = file_object.readlines()
# itemIds = set()
# for lin in lines:
#     if lin[0].isdigit() is False or len(lin.split("\t")) != 15:
#         print(lin)
# file_write.write(lin)
# file_write.flush()


def dealLog():
    file_object = open('D:\\logs\\nohup-current.log', "r", encoding='utf-8')
    file_write = open('D:\\logs\\nohup-current-1.log', "a", encoding='utf-8')
    lines = file_object.readlines()
    for lin in lines:
        if '自定义' in lin:
            file_write.write(lin)
            file_write.flush()


def statistical_data():
    sum_map = {}
    file_read = open('D:\\logs\\nohup-current-1.log', "r", encoding='utf-8')
    lines = file_read.readlines()
    for lin in lines:
        if '自定义' in lin and '处理完成' in lin:
            account = lin.split("<->")[2].split("-")[0].replace(" ", "")
            if sum_map.get(account) is None:
                sum_map[account] = 1
            else:
                sum_map[account] = sum_map[account] + 1

    print(sum_map)


def statistical_data_single_account():
    success = 0
    error = 0
    file_read = open('D:\\logs\\nohup-current-1.log', "r", encoding='utf-8')
    lines = file_read.readlines()
    for lin in lines:
        if '自定义' in lin and 'tb33821540' in lin:
            if '处理完成' in lin:
                success = success + 1
            elif '发生异常' in lin:
                error += 1
    print(success, error)


def parseAppText(itemId,text):
    coupons = []
    info = entity.AppBookInfo(itemId=itemId, defaultPrice=None, activePrice=None, coupons=None, free=None, sales=None,
                              originalText=text, name=None)
    text = text[3:]
    #先替换掉日期影响
    month = datetime.datetime.now().month
    match = re.search(str(month) + "月" + "(.+?)开卖", text)
    if match is not None:
        groups = match.group(0)
        text = text.replace(groups, "日期替换")

    # 活动价格
    match = re.search("￥(.+?)[\d.]+", text)
    if match is not None:
        groups = match.group(0)
        if groups is not None:
            search = re.search("\d(\d)*[\d.]*", groups)
            if search is not None:
                price = search.group(0)
                # 都赋值，后面价格定位替换
                info.activePrice = price
                info.defaultPrice = price
            else:
                info.activePrice = groups
                info.defaultPrice = groups
    # 券后价
    match = re.search("(券后|折后)￥(.+?)[\d.]+", text)
    if match is not None:
        groups = match.group(0)
        if groups is not None:
            search = re.search("\d(\d)*[\d.]*", groups)
            if search is not None:
                price = search.group(0)
                info.activePrice = price
            else:
                info.activePrice = groups
    match = re.search("价格￥(.+?)[\d.]+", text)
    if match != None:
        groups = match.group(0)
        if groups is not None:
            search = re.search("\d(\d)*[\d.]*", groups)
            if search is not None:
                price = search.group(0)
                info.defaultPrice = price
            else:
                info.defaultPrice = groups
    # 提取 “领券...领取” 中的内容
    match = re.search("领券(.+?)领取", text)
    if match != None:
        groups = match.group(0)
        coupons.append(groups)
    # 提取 “查看...领取” 中的内容
    match = re.search("查看(.+?)领取", text)
    if match != None:
        # 领券内容
        groups = match.group(0)
        coupons.append(groups)
    # 满减
    match = re.search("满(.+?)减(.+?)\d+", text)
    if match != None:
        groups = match.group(0)
        coupons.append(groups)
        # 包邮
    match = re.search("满(\d+?)享包邮", text)
    if match != None:
        groups = match.group(0)
        info.free = groups

    match = re.search(u"月销(.+?)\+", text)
    if match != None:
        groups = match.group(0)
        info.sales = groups
    match = re.search(u"月销(.+?)\d+", text)
    if match is not None:
        groups = match.group(0)
        info.sales = groups
    if len(coupons) > 0:
        info.coupons = (",".join(coupons))

    #print(info.toString())
    return info

def getName(text):
    if "큚" in text and "ꄪ" not in text:
        match = re.search(u"큚(.+?)+", text)
    else:
        match = re.search(u"큚(.+?)ꄪ", text)
    if match != None:
        groups = match.group(0)
        ignoTextGroups = re.search(u"큚(.+?)领取", groups)
        if ignoTextGroups != None:
            groups = groups.replace(ignoTextGroups.group(0), "")
        groups = groups.replace(" ", "").replace("큚", "").replace("ꄪ", "")
        return  groups
# if __name__ == '__main__':
#     # text="1/588狂欢价￥24.5活动期限时折后￥228月6日00:00开卖8.6 00:00-01:00超级秒杀跨店每200减20领券큚￥24.5  正版包邮 别想太多啦书在复杂的世界里做一个简单的人名取芳彦别想太多了日本畅销情绪疗愈指南人生哲学励志正能量书籍ꄪ分享"
#     # parseAppText(text=text,itemId="123")
#     # month = datetime.datetime.now().month
#     # nextMonth = month+1
#     # match = re.search(str(month)+"月"+"(.+?)开卖", text)
#     # if match is not None:
#     #     groups = match.group(0)
#     #     replace = text.replace(groups, "日期替换")
#     #     print(replace)
#     file_read = open('D:\\爬虫\\记录\\88价格提取错误.txt', "r", encoding='utf-8')
#     file_write = open('D:\\爬虫\\记录\\88价格提取错误-修复.txt', "w", encoding='utf-8')
#     lines = file_read.readlines()
#     for line in lines:
#         split = line.split("\t")
#         try:
#             info = parseAppText(itemId=split[0],text=split[1])
#             file_write.write(split[0] + "\t" + info.defaultPrice + "\t" + info.activePrice +"\n")
#         except:
#             print("ERRORLINE: "+line)
#             pass
#
#     # file_read = open('D:\\爬虫\\记录\\original-text.txt', "r", encoding='utf-8')
#     # file_write = open('D:\\爬虫\\记录\\original-text-2.txt', "w", encoding='utf-8')
#     # lines = file_read.readlines()
#     # for line in lines:
#     #     split = line.split("\t")
#     #     try:
#     #         split[0] = split[0].replace("\"","")
#     #         split[1] = split[1].replace("\"", "")
#     #     except:
#     #         pass
#     #     file_write.write(split[0]+" "+str(getName(split[1]))+"\n")
#
#     # match = re.search("^(\d.?)[\d.]+", text)
#     # group = match.group(0)
#     # print(group)

def loads_jsonp(_jsonp):
    try:
        find = _jsonp.find("TShop.Setup")
        return json.loads(re.match("TShop\\.Setup\\((.*)\\);", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')

def macth_brackets(text):
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

def macth_h5_detail(text):
    match = re.search("_DATA_Detail =(.*)};", text, re.S)
    text = match.group(0)
    stack = []
    match_s = "{"
    match_e = "}"
    jsonStr = ""
    start_index = text.find("_DATA_Detail = ") + len("_DATA_Detail = ")
    end_index = len(text) - 1
    for i in range(start_index, end_index):
        if text[i] == match_s:
            stack.append(i)
        if text[i] == match_e:
            stack.pop()
        if len(stack) == 0:
            jsonStr = text[start_index:i+1]
            break
    return jsonStr

def conver(book,key,value):
    if "书名" in key:
        book.setName(value.replace(" ", "").replace(" ", ""))
    if "ISBN" in key:
        book.setIsbn(value.replace("ISBN编号: ", "").replace(" ", ""))
    if ("作者" in key) or ("编者" in key):
        if "作者地区" not in key:
            book.setAuther(value.replace("作者: ", "").replace(" ", ""))
    if ("定价:" in key) or ("定价：" in key) or ("定价" in key):
        book.setFixPrice(value.replace("定价: ", "").replace("价格: ", "").replace("定价：", "").replace(" ", ""))
    if ("出版社" in key) or ("出版社" in key):
        book.setPress(value.replace("出版社名称:", "").replace(" ", "").replace(" ", ""))
        
def analySkuInfoJsonH5(json):
    sku_infos = []
    #skuID 和 propPath 的对应关系
    sku_id_map={}
    sku_name_map={}
    sku_price_map = {}
    skuBase = json.get("skuBase").get("skus")
    if skuBase is None or len(skuBase) ==0:
        return sku_infos
    #skuid-vid
    for temp in skuBase:
        sku_id_map.setdefault(temp.get("skuId"),temp.get("propPath").split(":")[1])
    # 取出skuID 对象的名称
    if json.get("skuBase").get("props") is not None and isinstance(json.get("skuBase").get("props"),list):
        for prop in json.get("skuBase").get("props"):
            skuBase = prop.get("values")
            for temp in skuBase:
                sku_name_map.setdefault(temp.get("vid"),temp.get("name"))
    if json.get("skuBase").get("props") is not None and isinstance(json.get("skuBase").get("props"),dict):
        skuBase = json.get("skuBase").get("props").get("values")
        for temp in skuBase:
            sku_name_map.setdefault(temp.get("vid"), temp.get("name"))
    #取出skuId 对应的价格
    skuBase = json.get("mock").get("skuCore").get("sku2info")
    for key,value in skuBase.items():
        sku_price_map.setdefault(key,value.get("price").get("priceText"))
    #组装
    for key,value in sku_id_map.items():
        info = SkuInfo(sku_id=None, spu_id=None, name=None, price=None)
        #获取价格
        info.sku_id=key
        info.name=sku_name_map.get(value)
        info.price=sku_price_map.get(key)
    return sku_infos

if __name__ == '__main__':
    proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']

    # print(proxyIp)
    # proxy = {'http': "http://" + proxyIp, 'https': "https://" + proxyIp}
    # session = HTMLSession()
    # detailResponse = session.get("http://httpbin.org/ip", proxies=proxy)
    # print(detailResponse.text)
    # session = HTMLSession()
    # get = session.get(
    #     "http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=11&pack=181521&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4")
    # ip = get.text.replace("\r", "").replace("\n", "")
    #
    #
    #ip = "42.57.151.173:4278"

    # session = HTMLSession()
    # detailResponse = session.get("http://httpbin.org/ip", proxies=proxy)
    # #detailResponse = session.get("http://httpbin.org/ip")
    # print(detailResponse.text)
    proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
    tempHeaders = {
        "cookie":"hng=CN%7Czh-CN%7CCNY%7C156; miid=2308380591735044775; OZ_1U_2061=vid=v0dc113aa9e628.0&ctime=1626253285&ltime=1626251577; _uab_collina=163176095720886309866329; cna=lf7KGSbBLWICAXAuRv5KSRT5; t=6eea51d2023af5f8b189f7a42098ab7d; _tb_token_=e133fe53e5f3e; cookie2=1cc2deae226c103e2af9d331b3ba0cf7; xlly_s=1; dnk=starlpwba; uc1=cookie15=UtASsssmOIJ0bQ%3D%3D&cookie21=VT5L2FSpccLvQjsn%2FRsa&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie14=Uoe3dYeA3Ie8Pg%3D%3D&pas=0&existShop=false; uc3=nk2=EEo%2Bp%2FLK58jc&id2=UUkPJL%2B7%2B962Hg%3D%3D&lg2=VT5L2FSpMGV7TQ%3D%3D&vt3=F8dCujaJqoWvvwXZk0I%3D; tracknick=starlpwba; lid=starlpwba; uc4=nk4=0%40EpM1dMmt7RMYXlGxkrLgGLNgaa0%3D&id4=0%40U2uDcV6ImQfsGvqMv8rADKr5ZU20; _l_g_=Ug%3D%3D; unb=2115355958; lgc=starlpwba; cookie1=AHspna58nSMPuxsW597yfuDVzyAexrcnCkoHNvFa7wQ%3D; login=true; cookie17=UUkPJL%2B7%2B962Hg%3D%3D; _nk_=starlpwba; sgcookie=E100KANtI6NGC650L%2BKs01wI9y8kwCLnOs4lJELF1f3SustSdzD8Eb5tWbWEHNfu4e44MkRnPXSyOuIo5bqo1gyFwOQ93aW5ZadB%2Bhl2F5RPvnQ%3D; cancelledSubSites=empty; sg=a8b; csg=29c53f93; enc=xg3%2B0ozu62eQWxUJx8wIy8a6d7aZCVHH2sInbi51RXkWKqWucgMWX3oUlFaeY8cj3uYas7%2BGlG%2BRSOD5X1ZXbA%3D%3D; cq=ccp%3D0; pnm_cku822=098%23E1hvF9vUvbpvUpCkvvvvvjiWPsqOsjl8PLMwgjEUPmPh1jE2PL5W0jY8RLSyQjlWRQgCvvpvvPMMvvhvC9vhvvCvpb9Cvm9vvvvvphvvvvvv99Cvpv9HvvmmvhCvmhWvvUUvphvUI9vv99CvpvkkkvhvC99vvOCtou9Cvv9vvUv%2FOnS%2B%2Fv9CvhQWrXgvC0RxCaV9%2Bul08ToQD70OVC69D7zyaX44ah7QD7zydigLXGeDKX6cWsEarp033Le3b6KxIExreC9anbmxfamK5kx%2F6j7%2BD40wRvhvCvvvvvmevpvhvvmv99%3D%3D; tfstk=c_XOBQ9-dy4itIKd41F3cME6vtWAZYk9kcTrHkQLnU_b5HMAizWle9kL1339pkC..; l=eBMCAbpugsEP5udsBOfZnurza779IIRAguPzaNbMiOCPOyf65Y3RW6eYKiTBCnGVh6SWR37gE--uBeYBqID6rVm1a6Fy_Ckmn; isg=BOTkVrgGWQd1va3LqaA8C6SkteLWfQjnDE3d__4Fcq9yqYRzJokQd6sLbQGxcUA_",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    proxyIp = "111.126.77.179:4245"
    proxy = {'http': "http://" + proxyIp, 'https': "https://" + proxyIp}
    session = HTMLSession()
    #detailResponse = session.get("https://detail.tmall.com/item.htm?id=556741761245&rn=5f6fa8b61661c51c2643703c00330a43&abbucket=17", headers=tempHeaders, proxies=proxy)
    detailResponse = session.get("https://detail.m.tmall.com/templatesNew/index?id=653510659650", proxies=proxy)
    detailHtmlSoup = BeautifulSoup(detailResponse.text.encode("utf-8"), features='html.parser')
    print(detailResponse.text)
    detail = macth_h5_detail(detailResponse.text)
    loads = json.loads(detail)
    print(detail)
    detail = macth_h5_detail(detailResponse.text)
    detailJson = json.loads(detail)
    baseDetails = detailJson.get("props").get("groupProps")[0].get("基本信息")
    book = Book(tmId=None, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                promotionPriceDesc=None, price=None, promotionType=None, activeStartTime=None,
                activeEndTime=None,
                activeDesc="", shopName=None, category=None, sales="0", press=None,
                skuId=None, skuName=None)
    for temp in baseDetails:
        for key,value in temp.items():
            print(key,value)
            conver(book,key,value)
    #print(book.toString())
    h_ = analySkuInfoJsonH5(detailJson)

    # match= re.search("TShop\\.Setup\\((.*)\\);", detailResponse.text, re.S)
    # text = match.group(0)
    # match = re.match("TShop\\.Setup\\((.*)\\);", text, re.S)
    # print(text)
    # macth_brackets(text)











