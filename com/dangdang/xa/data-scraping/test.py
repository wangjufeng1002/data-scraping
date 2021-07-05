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

if __name__ == '__main__':
    statistical_data_single_account()