import requests
import urllib.parse

from bs4 import BeautifulSoup


def search(words,cookie,shop_url):
    headers = {"cookie": cookie}
    keyword = urllib.parse.quote(words.encode("gb2312"))
    res = requests.get(shop_url.format(keyword), headers=headers)
    return  res.text

def parse_html(html):
    soup = BeautifulSoup(html, features='html.parser')
    find_all = soup.find_all(name="a", attrs={"class": "J_TGoldData"})
    detailUrl = []
    for el in find_all:
        detail_url = el.attrs['href']
        detailUrl.append(detail_url)
    return detailUrl
if __name__ == '__main__':
    cookie = "cna=jV6JGV+u1jwCAXAuRv4HVlx5; sm4=610100; t=e4725ef2abf6b5248fad8557010aac73; _tb_token_=171e3b734eaf; cookie2=11d9356446ab0d34c1540f753192c2ae; _m_h5_tk=acb099aabdf87dd49a62a8e4f9e09268_1629710155643; _m_h5_tk_enc=db5d36942cd5d870319dd20d4e785b65; dnk=%5Cu98CE%5Cu98CE%5Cu98CE%5Cu6211%5Cu662F%5Cu75AF%5Cu513F%5Cu514B; tracknick=%5Cu98CE%5Cu98CE%5Cu98CE%5Cu6211%5Cu662F%5Cu75AF%5Cu513F%5Cu514B; lid=%E9%A3%8E%E9%A3%8E%E9%A3%8E%E6%88%91%E6%98%AF%E7%96%AF%E5%84%BF%E5%85%8B; lgc=%5Cu98CE%5Cu98CE%5Cu98CE%5Cu6211%5Cu662F%5Cu75AF%5Cu513F%5Cu514B; login=true; cancelledSubSites=empty; pnm_cku822=; sn=%E5%BD%93%E5%BD%93%E7%BD%91%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%8A%80%E6%9C%AF; _l_g_=Ug%3D%3D; unb=2132825584; cookie1=BYiMchvXw%2FnYQFh5FTbi%2FAMSYco3nQz%2BBGWeWJGxVvQ%3D; cookie17=UUkNZrtascymbw%3D%3D; _nk_=%5Cu98CE%5Cu98CE%5Cu98CE%5Cu6211%5Cu662F%5Cu75AF%5Cu513F%5Cu514B; sg=%E5%85%8B48; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie15=V32FPkk%2Fw0dUvg%3D%3D&cookie14=Uoe2xMRLylK75w%3D%3D&pas=0&existShop=false&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=U%2BGCWk%2F7p4mAie9u%2F8FK; uc3=id2=UUkNZrtascymbw%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D&nk2=1CBFZPp3QNb9ekfF7Vo3yA%3D%3D&vt3=F8dCujHvEWF2pNyxcis%3D; uc4=id4=0%40U2uBbcOkve5T70VGKhSXBkj9adpt&nk4=0%401vFhnBRCcDwT%2F0VH%2FHmOQTrhMefz0mgznWt2; sgcookie=E1008irkPW4eaIo5t4cOtP9So4cJdYYXcmpDaz12ZXpswu%2Fo43ISs70ep8aUPemPHNgr457%2F6PaMeePUtoTVTEMsgn5mVHs%2BYXsuy7pPN9Vn5HE%3D; csg=216bdcf0; enc=eC%2BF%2F9gWhBeWChdGym%2FOS35AHyPGACU8ixAwzX5x9a1fJ2KRIAqneyw3AX8VBUgA6lweFuWAqXg9n3p4CPxdQA%3D%3D; xlly_s=1; tfstk=cIbcBAG04i-jzetlArTfg61DeryRZdnJHHKlzNBJEkt9GLQPixnrYlOihLXcWc1..; l=eBgg6qMVgOl2ZlRhBOfZourza779YIRAguPzaNbMiOCPOs1eSW9cW6nR7w8wCnGVh62HR3SW3fIbBeYBqnfOov33zpGkgIDmn; isg=BI-P0aEOMqLzCzZ44UMac3NuHiOZtOPWpX8ARKGceP4PcK9yqYT9JkhmcqBOCLtO"
    url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1629789747769_170&callback=jsonp171&mid=w-23389038992-0&wid=23389038992&path=/view_shop.htm&userId=null&shopId=57300329&view_type=null&order_type=null&spm=0&search=y&keyword={}"
    res=search("人间失格",cookie,url)
    html=res[res.find('<img height='):res.rfind('")')-2].encode('gbk')
    print(html)
    urls=parse_html(html)
    print(urls)