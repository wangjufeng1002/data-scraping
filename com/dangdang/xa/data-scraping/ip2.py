import urllib.request as res
import time, random

import requests

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


itemUrl = 'https://detail.tmall.com/item.htm?id=620523822174&rn=6e9c59d750b2592eef375d7c778ce71d&abbucket=11'
proxy ={'http':'http://106.14.198.6:8080','https':'https://106.14.198.6:8080'}
session = HTMLSession()
detailResponse = session.get(url,headers=headers, proxies=proxy,timeout=10)
print(detailResponse.text)
print(detailResponse.status_code)


requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()

s.keep_alive = False  # 关闭多余连接
proxy = {'http:': 'http://8B44078D0103044E:7FD3CE9AC11E@27.152.192.18:60221', 'https:': 'https://8B44078D0103044E:7FD3CE9AC11E@27.152.192.18:60221'}
s.proxies=proxy
detailResponse = s.get(url=url)
print(detailResponse.text)





# response=requests.get("http://httpbin.org/ip",proxies={'http://':'DANGDANG:dangdangcmt@140.255.42.246:57114'})
# print(response.text)
