import re
import random

import requests
import urllib.parse
import MyLog
from bs4 import BeautifulSoup
import db

log = MyLog.Logger('search').get_log()


def search(words, cookies, shop_url):
    headers = {"cookie": cookies}
    keyword = urllib.parse.quote(words.encode("gb2312"))
    response = requests.get(shop_url.format(keyword), headers=headers)
    return response.text


def parse_html(html_body):
    soup = BeautifulSoup(html_body, features='html.parser')
    find_all = soup.find_all(name="a", attrs={"class": "J_TGoldData"})
    detailUrl = []
    for el in find_all:
        uri = el.attrs['href']
        if uri is not None:
            item_id = re.match(".*?(id=.*&).*", uri, re.S).group(1).split('&')[0].replace('id=', '')
            item_url = "http:" + uri
            itemUrl = {"url": item_url, "id": item_id}
            detailUrl.append(itemUrl)
    return detailUrl


def search_api(words, shop_name):
    log.info("开始在店铺:%s搜索%s", shop_name, words)
    cookies = db.get_cookies()
    cookie = cookies[random.randint(0, len(cookies) - 1)]
    #更新一下最后修改时间
    db.update_cookies_status(1, cookie['id'])
    log.info("获取到的cookie是%s", cookie)
    url = db.get_url_by_shop_name(shop_name)['search_url']
    log.info("shop_name:%s的搜索url是:%s", shop_name, url)
    res = search(words, cookie['cookies'], url)
    html = res[res.find('<img height='):res.rfind('")') - 2]
    html = html.replace("\\", "")
    data = parse_html(html)
    if len(data) == 0:
        log.info("cookies 失效,", cookie)
        db.update_cookies_status(-1,cookie['id'])
        return
    for item in data:
        log.info("item:%s", item)
        book = db.get_book_url(item['id'])
        if book is None:
            db.insert_book_url(item['url'], item['id'], shop_name)
