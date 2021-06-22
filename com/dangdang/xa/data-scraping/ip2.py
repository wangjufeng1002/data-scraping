import urllib.request as res
import time, random

import requests

from requests_html import HTMLSession, AsyncHTMLSession
#访问的网址
url = "http://httpbin.org/ip"
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
proxy ={'http':'http://8B44078D0103044E:7FD3CE9AC11E@36.62.194.183:18714','https':'https://8B44078D0103044E:7FD3CE9AC11E@36.62.194.183:18714'}
session = HTMLSession()
itemUrl = 'http://detail.tmall.com/item.htm?id=614136075461&rn=ace0ac91189f544329f55e731c8c1b7f&abbucket=11'
detailResponse = session.get(itemUrl,headers=headers, proxies=proxy)
print(detailResponse.text)
print(detailResponse.status_code)





# response=requests.get("http://httpbin.org/ip",proxies={'http://':'DANGDANG:dangdangcmt@140.255.42.246:57114'})
# print(response.text)
