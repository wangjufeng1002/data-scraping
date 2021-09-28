from bs4 import BeautifulSoup
from requests_html import HTMLSession, AsyncHTMLSession

if __name__ == '__main__':
   startprice=1
   formaturl = "https://muduots.tmall.com/search.htm?tsearch=y&search=y&orderType=hotsell_desc&viewType=grid&keyword=&lowPrice={}&highPrice={}"
   for i in range(1,20):
       url = formaturl.format(str("%.2f" % startprice),str("%.2f" % (startprice+0.1)))
       startprice=startprice+0.1
       print(url)

