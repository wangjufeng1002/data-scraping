from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
import threading, time
import getIpProxyPool

#if __name__ == '__main__':
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

    #file_object = open('D:\\爬虫\\TM\\remote\\TM\\1\\item-detail-base-x.txt', "r", encoding='utf-8')
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
        if '自定义' in lin and '处理完成' in lin :
            account = lin.split("<->")[2].split("-")[0].replace(" ", "")
            if sum_map.get(account) is None:
                sum_map[account] = 1
            else:
                sum_map[account] = sum_map[account]+1

    print(sum_map)

def statistical_data_single_account():
    success = 0
    error =0
    file_read = open('D:\\logs\\nohup-current-1.log', "r", encoding='utf-8')
    lines = file_read.readlines()
    for lin in lines:
        if '自定义' in lin and 'tb33821540' in lin:
           if '处理完成' in lin :
               success =success +1
           elif '发生异常' in lin:
                error +=1
    print(success,error)
def parseAppText(text):
    constants=[]
    # 价格
    match = re.search("￥(.+?)[\d.]+", text)
    if match != None:
        # 领券内容
        groups = match.group(0)
        # print(groups)
        constants.append(groups)
    # 券后价
    match = re.search("券后(.+?)[\d.]+", text)
    if match != None:
        groups = match.group(0)
        # print(groups)
        constants.append(groups)
    match = re.search("价格(.+?)[\d.]+", text)
    if match != None:
        groups = match.group(0)
        # print(groups)
        constants.append(groups)
    #提取 “领券...领取” 中的内容
    match = re.search("领券(.+?)领取", text)
    if match != None:
        groups = match.group(0)
        constants.append(groups)
    # 提取 “查看...领取” 中的内容
    match = re.search("查看(.+?)领取", text)
    if match != None:
        # 领券内容
        groups = match.group(0)
        #print(groups)
        constants.append(groups)

    #包邮
    match = re.search("满(\d+?)享包邮", text)
    if match != None:
        groups = match.group(0)
        #print(groups)
        constants.append(groups)
        # 包邮
    #满减
    match = re.search("满(.+?)减(.+?)\d+", text)
    if match != None:
        groups = match.group(0)
        constants.append(groups)
        #print(groups)
    #销量
    match = re.search(u"月销(.+?)(\+|\d+)", text)
    if match != None:
        groups = match.group(0)
        constants.append(groups)
        #print(groups)
   # splits = text.split("큚")
   # splits = text.split("큚")
    print(constants)

    #print(splits)
if __name__ == '__main__':
    text="1/6专属优惠￥27.2券后￥22.2满88享包邮购买得积分查看큚￥5官方补贴红包实物商品，满5.01元通用已领取  窗边的小豆豆 正版书 黑柳彻子小学生三年级五年级四年级阅读课外书非注音版故事书 图书名著新华书店旗舰店官网 窗边的小豆豆ꄪ分享爱心树优质童书小学五年级适用学龄段推荐帮我选"
    parseAppText(text=text)