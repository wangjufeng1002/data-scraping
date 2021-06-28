from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book, ItemUrl, Logger
import threading, time
import getIpProxyPool
promotionUrl = 'https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false&itemId={itemId}&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621928176000&isRegionLevel=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&timestamp=1622029723119&isg=eBIE8Mulj-IREQ65BOfChurza779JIRYjuPzaNbMiOCP_Hf671mVW6sFIY8BCnGVh6AwJ3oiiBs_BeYBq_C-nxvOa6Fy_3Hmn&isg2=BPz8DUnnsCHnEoT3_AthiILwzZqu9aAfdLEeZdZ9POfMoZwr_wX0r_dQgcnZ0th3'

header={
    "cookie":
    "hng=CN%7Czh-CN%7CCNY%7C156; t=087cd7302c92ae497e5e94ef10e5ad74; enc=L3vmwJf7sww7FFWljQdOqaAUX1B%2BKROSzXWqhMNNSU0ejFy5C2K%2FiwMRNvNRdOciF0HDhp2cxxpOtpKqNFL3fg%3D%3D; _samesite_flag_=true; cookie2=129eb0f05c043f4d75d74fc69320ac97; _tb_token_=5eebb5305be55; _m_h5_tk=17eb8f19b3a10568c32f573e06b90ec4_1624620054068; _m_h5_tk_enc=41778cd52184a475b9d09f7aede3b505; xlly_s=1; mt=ci=0_0; cna=z2XMGGMVbRoCAXAuRv5JFOGI; unb=3197147351; uc1=cookie21=Vq8l%2BKCLiYYu&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&pas=0&cookie14=Uoe2ySEWsQ4P9Q%3D%3D&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false; uc3=vt3=F8dCuwziOT4hD%2FiwbM4%3D&id2=UNGfEU%2BirkacyA%3D%3D&nk2=GdBtF%2BckV1I%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; csg=54ca26ef; lgc=zxc90028; cookie17=UNGfEU%2BirkacyA%3D%3D; sgcookie=E1000zUsp5Uk4YmLo3vBNMceQEvl3RjA6DQrFyuOEeQa4W2WICwhkYLOFuoCxiwKmq7WBd4vxPv9S6ntlzTzki%2BA4w%3D%3D; dnk=zxc90028; skt=989255a5f211b687; existShop=MTYyNDYyMjE4OQ%3D%3D; uc4=id4=0%40UgbnmKjksSJTYuijmzvwt6jJdBsz&nk4=0%40GxlRMZgRosmxMEd9o79fAkgKOw%3D%3D; tracknick=zxc90028; _cc_=VFC%2FuZ9ajQ%3D%3D; _l_g_=Ug%3D%3D; sg=81c; _nk_=zxc90028; cookie1=V3ofTsOhBP752p3u6tRpZK5fSCeqcieKQ7MAHlXqFcY%3D; x5sec=7b226d616c6c64657461696c736b69703b32223a223432373962313336363162333439383638633766373637616566663332636239434b4b4a31345947454d5451734e7278684958667851456144444d784f5463784e44637a4e5445374d54443874736d4e41673d3d227d; isg=BLe3W7kxm1uRIx_TYCk1_47cRqsBfIvekbsedglk-wbtuNb6EUxVLpTZmhjmV2NW",
    "referer": "https://detail.tmall.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}
url="https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false&itemId=14265914964&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1624570038000&isRegionLevel=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&timestamp=1624622303205&isg=eBIE8Mulj-IREV91BO5Churza779PIdbz1PzaNbMiInca6Td1FhenNCBFxw2Rdtjgt5AkeKP1ooqrRnWSyaU-AkDBeYCKXIpBavMRe1..&isg2=BE1Nka2MEfm_0bWkheQgyztXXGnHKoH8_7X09I_TLeRfhm84VnnLzQBX8BrgQZm0&ref=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fid%3D14265914964%26rn%3Dfc1bccd66bb2d9d0e1d0d7d8b197ba85%26abbucket%3D10"
session = HTMLSession()
promotionJsonp = session.get(promotionUrl.format(itemId=548095984505),headers=header)

print(promotionJsonp)