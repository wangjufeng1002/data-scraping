#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import ItemUrl, Logger
import threading, time
import logging
import constants

# 综合排序
wenxuan_url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1622799637450_126&callback=jsonp127&mid=w-23389038992-0&wid=23389038992&path=/category-491550351.htm&spm=a1z10.3-b-s.w4011-23389038992.126.48c57652OYn3TO&catId=491550351&pageNo={pageNo}&tsearch=y&scid=491550351"
# 销量排序
wenxuan_sale_url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1622014477031_126&callback=jsonp&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.272.73b67652D3iZj3&pageNo={pageNo}&tsearch=y"
# 新品排序
wenxuan_new_url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1622014553749_126&callback=jsonp&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.288.22787652dTswMv&orderType=newOn_desc&pageNo={pageNo}&tsearch=y"
# 价格排序
wenxuan_price_url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1622014553749_126&callback=jsonp&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.288.22787652dTswMv&orderType=price_asc&pageNo={pageNo}&tsearch=y"

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

logUtils = Logger(filename='./logs/wenxuan-url.log', level='info')
#dataReptiledb.host="192.168.47.210"
dataReptiledb.host="127.0.0.1"

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
    dataReptiledb.insertItemUrl(item_urls)


# 干扰函数
def disturbUrl(header, ip):
    time.sleep(random.randint(1, 5))
    randint = random.randint(1, 10)
    if randint % 2 == 0:
        session = HTMLSession()
        session.get(url=random.choice(url), headers=header,
                    proxies={'http': ip})
        logUtils.logger.info("{thread} 执行一次 其他请求 ".format(thread=threading.current_thread().getName()))


def process_page_list(url, category):
    headers = dataReptiledb.getHeaders()
    headerIndex = 0
    ip_list = dataReptiledb.getIpList()
    # 获取要处理的页数
    page_pool = dataReptiledb.getPageRecords(shopId=1, isSuccess=0, category=category)
    successPagePool = set()
    while True:
        if page_pool is None or len(page_pool) <= 0:
            return
        tempPage = random.choice(page_pool)
        # 再成功的 页数记录中存在
        if tempPage is successPagePool:
            continue
        session = HTMLSession()
        logUtils.logger.info(
            "{thread}线程 开始抓取第 {page}页 {time} ".format(thread=threading.current_thread().getName(), page=tempPage,
                                                      time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        try:
            url_format = url.format(pageNo=tempPage)
            listResult = session.get(url=url_format, headers=headers[headerIndex],
                                     proxies={'http': random.choice(ip_list)})
            listResult.encoding = "utf-8"
            detailUrl = eval(listResult.text)
            detailUrl = list(set(detailUrl))
            logUtils.logger.info(
                "{thread}线程 抓取第 {page}页完成 {time},{size} ".format(thread=threading.current_thread().getName(), page=tempPage,
                                                          time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),size=len(detailUrl)))
            # 干扰函数
            try:
                disturbUrl(headers[headerIndex], random.choice(ip_list))
            except:
                logUtils.logger.error("其他请求发生异常")
                write_db(detailUrl=detailUrl, shopName="新华文轩网络书店", category=category)
        except Exception as e:
            # 干扰函数
            disturbUrl(headers[headerIndex], random.choice(ip_list))
            # 更新库 ，，查询新的
            dataReptiledb.updatePageRecordsBatch(successPagePool, 1, 1, category)
            # 清空成功 页数池
            successPagePool.clear()
            # 重新查询
            page_pool = dataReptiledb.getPageRecords(1, 0, category)
            # record_file.write(getPageNum)
            logUtils.logger.error(" %s 线程 抓取第 %d页 发生了一些异常 ： %s " % (threading.current_thread().getName(), tempPage, e))
            if headerIndex == len(headers) - 1:
                ip_list = dataReptiledb.getIpList()
                headers = dataReptiledb.getHeaders()
                headerIndex = 0
            else:
                ip_list = dataReptiledb.getIpList()
                headerIndex += 1
            # 异常休眠 5秒
            time.sleep(20)
            continue
        else:
            write_db(detailUrl=detailUrl, shopName="新华文轩网络书店", category=category)
            successPagePool.add(tempPage)
            if len(page_pool) != 0:
                # 移除这个
                page_pool.remove(tempPage)
            if len(successPagePool) >= 5 or len(page_pool) < 5:
                # 更新库 ，，查询新的
                dataReptiledb.updatePageRecordsBatch(successPagePool, 1, 1, category)
                # 清空成功 页数池
                successPagePool.clear()
                # 重新查询
                page_pool = dataReptiledb.getPageRecords(1, 0, category)
            time.sleep(random.randint(10, 20))


if __name__ == '__main__':
    #thread_1 = threading.Thread(target=process_page_list, args=(constants.w_wx, 'wx'), name="文学").start()
    #thread_2 = threading.Thread(target=process_page_list, args=(constants.w_jf, 'jf'), name="教辅").start()
    #thread_3 = threading.Thread(target=process_page_list, args=(constants.w_ts, 'ts'), name="童书").start()
    # thread_4 = threading.Thread(target=process_page_list, args=(constants.w_ts, 'cglz'), name="成功励志").start()
    # thread_5 = threading.Thread(target=process_page_list, args=(constants.w_ts, 'kj'), name="科技").start()
    # thread_6 = threading.Thread(target=process_page_list, args=(constants.w_ts, 'jjgl'), name="经济管理").start()
    # thread_7 = threading.Thread(target=process_page_list, args=(constants.w_ts, 'yssy'), name="艺术与摄影").start()
    # thread_9 = threading.Thread(target=process_page_list, args=(constants.w_ts, 'rwsk'), name="人文社科 ").start()
    # thread_10 = threading.Thread(target=process_page_list, args=(constants.w_ts, 'sezj'), name="少儿早教 ").start()

    threading.Thread(target=process_page_list, args=(constants.文学, '文学'), name="文学").start()
    threading.Thread(target=process_page_list, args=(constants.小说, '小说'), name="小说 ").start()
    threading.Thread(target=process_page_list, args=(constants.动漫绘本, '动漫绘本'), name="动漫绘本 ").start()
    threading.Thread(target=process_page_list, args=(constants.超低价区, '超低价区'), name="超低价区 ").start()
    threading.Thread(target=process_page_list, args=(constants.少儿, '少儿'), name="少儿 ").start()
    threading.Thread(target=process_page_list, args=(constants.英语与其他外语, '英语与其他外语'), name="英语与其他外语 ").start()


    threading.Thread(target=process_page_list, args=(constants.辞典与工具书, '辞典与工具书'), name="辞典与工具书 ").start()
    threading.Thread(target=process_page_list, args=(constants.医学, '医学'), name="医学 ").start()
    threading.Thread(target=process_page_list, args=(constants.经济, '经济'), name="经济 ").start()
    threading.Thread(target=process_page_list, args=(constants.管理, '管理'), name="管理 ").start()
    threading.Thread(target=process_page_list, args=(constants.励志与成功, '励志与成功'), name="励志与成功 ").start()
    threading.Thread(target=process_page_list, args=(constants.计算机与互联网, '计算机与互联网'), name="计算机与互联网 ").start()
    threading.Thread(target=process_page_list, args=(constants.社会科学, '社会科学'), name="社会科学 ").start()
    threading.Thread(target=process_page_list, args=(constants.科技, '科技'), name="科技 ").start()
    threading.Thread(target=process_page_list, args=(constants.建筑, '建筑'), name="建筑 ").start()
    threading.Thread(target=process_page_list, args=(constants.旅游, '旅游'), name="旅游 ").start()
    threading.Thread(target=process_page_list, args=(constants.哲学, '哲学'), name="哲学 ").start()
