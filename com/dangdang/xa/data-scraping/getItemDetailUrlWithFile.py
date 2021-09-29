#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime

import pymysql
from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import ItemUrl, Logger
import threading, time
import logging
import constants
import os
dataReptiledb.host="192.168.47.210"

logUtils = Logger(filename='./logs/wenxuan-url.log', level='info')
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

def jsonp(str):
    detailUrl = []
    soup = BeautifulSoup(str, features='html.parser')
    find_all = soup.find_all(name="a", attrs={"class": "J_TGoldData"})
    for el in find_all:
        detail_url = el.attrs['href']
        detailUrl.append(detail_url)
    return detailUrl


def write_db(detailUrl, shopName, category):

    item_urls = []
    for url in detailUrl:
        if url is not None:
            item_id = re.match(".*?(id=.*&).*", url, re.S).group(1).split('&')[0].replace('id=', '')
            item_url = "http:" + url
            itemUrl = ItemUrl(itemId=item_id, itemUrl=item_url, shopName=shopName, category=category)
            item_urls.append(itemUrl)
    # with open("res.txt",'a+',encoding='utf-8') as files:
    #     for item in item_urls:
    #         files.write(item.toString()+"\n")
    dataReptiledb.insertItemUrl(item_urls)


allpath = []
allname = []

def getallfile(path):
    allfilelist = os.listdir(path)
    # 遍历该文件夹下的所有目录或者文件
    for file in allfilelist:
        filepath = os.path.join(path, file)
        # 如果是文件夹，递归调用函数
        if os.path.isdir(filepath):
            getallfile(filepath)
        # 如果不是文件夹，保存文件路径及文件名
        elif os.path.isfile(filepath):
            allpath.append(filepath)
            allname.append(file)
    return allpath, allname

def processTxtUrl(path,category):
    file = open(path, encoding='utf-8')
    read = file.read().replace("undefined", "")
    soup = BeautifulSoup(read, features='html.parser')
    find_all = soup.find_all(name="a", attrs={"class": "J_TGoldData"})
    detailUrl = []
    for el in find_all:
        detail_url = el.attrs['href']
        detailUrl.append(detail_url)
    detailUrl = list(set(detailUrl))
    write_db(detailUrl=detailUrl, shopName="木垛旗舰店", category=category)


if __name__ == '__main__':


    rootdir='D:\chrome-downloads'
    files,names=getallfile(rootdir)
    for file in files:
        print(file)
        processTxtUrl(file,"null")
