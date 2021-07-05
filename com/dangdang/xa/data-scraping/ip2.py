import urllib.request as res
import time, random
from bs4 import BeautifulSoup
import json, re, demjson
import requests
import getIpProxyPool

from requests_html import HTMLSession, AsyncHTMLSession
#访问的网址
#创建ProxyHandler
proxy_port = res.ProxyHandler({'http':'8B44078D0103044E:7FD3CE9AC11E@117.31.45.58:36483'})
#创建opener
opener = res.build_opener(proxy_port)


tunnel = random.randint(1,10000)

headers = {"Proxy-Tunnel": str(tunnel)}



#添加User-Agent   这个添加User-Agent也可以在下面的urlopen中添加
# opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0')]
# #安装User Angent
# res.install_opener(opener)
# #使用自己安装好的opener
# response = res.urlopen(url)
# html = response.read().decode('utf-8')
# print(html)

url = "http://httpbin.org/ip"

# proxyIp = getIpProxyPool.get_proxy_from_redis()['proxy_detail']['ip']
# itemUrl = 'http://detail.tmall.com/item.htm?id=37209444242&rn=766e540483b8762c2181754e0fb2fab6&abbucket=10'
# session = HTMLSession()
# proxy = {'http:': "http://" + proxyIp, 'https:': "https://" + proxyIp}
# detailResponse = session.get(itemUrl,headers=headers,timeout=10)
# detailHtmlSoup = BeautifulSoup(detailResponse.text, features='html.parser')
# itmDescUl = detailHtmlSoup.find_all(name="ul", attrs={"id": "J_AttrUL"})
# contents = itmDescUl[0].contents
# for con in contents:
#     if "书名" in con.next:
#         print(con.next.replace("书名: ", ""))
#     if "ISBN" in con.next:
#         print(con.next.replace("ISBN编号: ", ""))
#     if ("作者" in con.next) or ("编者" in con.next):
#         if "作者地区" not in con.next:
#             print(con.next.replace("作者: ", "").replace("编者: ", ""))
#     if ("定价:" in con.next) or ("定价：" in con.next):
#         print(con.next.replace("定价: ", "").replace("价格: ", "").replace("定价：", ""))
#     if ("出版社" in con.next) or ("出版社" in con.next):
#         print(con.next.replace("出版社名称:", ""))
# print(detailResponse.status_code)


# requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
# s = requests.session()
#
# s.keep_alive = False  # 关闭多余连接
# proxy = {'http:': 'http://8B44078D0103044E:7FD3CE9AC11E@27.152.192.18:60221', 'https:': 'https://8B44078D0103044E:7FD3CE9AC11E@27.152.192.18:60221'}
# s.proxies=proxy
# detailResponse = s.get(url=url)
# print(detailResponse.text)





# response=requests.get("http://httpbin.org/ip",proxies={'http://':'DANGDANG:dangdangcmt@140.255.42.246:57114'})
# print(response.text)
#item-detail-base.txt ok
#item-detail-base-01.txt now
#item-detail-base-bowen.txt


if __name__ == '__main__':
    file_object = open('D:\\爬虫\\TM\\remote\\TM\\item-detail-base-bowen.txt', "r", encoding='utf-8')
    lines = file_object.readlines()
    for lin in lines:
        if lin[0].isdigit() is False or lin.split("\t")[5][0].isdigit() is False :
            print(lin[0:20])

        if len(lin.split("\t"))>16:
            print(lin)


