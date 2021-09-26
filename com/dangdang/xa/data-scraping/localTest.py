from bs4 import BeautifulSoup
from requests_html import HTMLSession, AsyncHTMLSession

if __name__ == '__main__':

    session = HTMLSession()
    detailResponse = session.get(
        "https://detail.tmall.com/item.htm?id=639273188572&rn=ee05056c4d5f08774e1c67ee62f7b955&abbucket=4")
    detailHtmlSoup = BeautifulSoup(detailResponse.text.encode("utf-8"), features='html.parser')
    print(detailResponse.text)
