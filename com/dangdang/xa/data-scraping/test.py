from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
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




if __name__ == '__main__':
    proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
    # print(proxyIp)
    proxy = {'http': "http://" + proxyIp, 'https': "https://" + proxyIp}
    # #proxy = {'http://':  proxyIp, 'https://': proxyIp}
    session = HTMLSession()
    #detailResponse = session.get("http://httpbin.org/ip", proxies=proxy)
    detailResponse = session.get("https://detail.tmall.com/item.htm?id=41903097818", proxies=proxy)
    detailHtmlSoup = BeautifulSoup(detailResponse.text.encode("utf-8"), features='html.parser')
    match= re.search("TShop\\.Setup\\((.*)\\);", detailResponse.text, re.S)
    text = match.group(0)
    match = re.match("TShop\\.Setup\\((.*)\\);", text, re.S)
    print(text)
    macth_brackets(text)











