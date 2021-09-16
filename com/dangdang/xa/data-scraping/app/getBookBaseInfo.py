import uiautomator2 as u2
import time
import multiprocessing
import threading
import MyLog
from timeit import default_timer
import db
from  entity import Book
log = MyLog.Logger('CMT').get_log()

def conver_save_book_info(item,detail_map):
    if item is None or detail_map is None or len(detail_map) == 0:
        return
    item_id = item.get("item_id")
    shop_name = item.get("shop_name")
    category = item.get("category")
    book = Book(tmId=item_id, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                promotionPriceDesc=None, price=0, promotionType=None, activeStartTime=None,
                activeEndTime=None,
                activeDesc=None, shopName=shop_name, category=category, sales="0",
                press=None)
    detail_map_infos = detail_map.items()
    for key ,value in detail_map_infos:
        if "书名" in key:
            book.setName(value.replace("书名: ", ""))
        elif "ISBN" in key:
            book.setIsbn(value.replace("ISBN编号: ", ""))
        elif ("作者" in key) or ("编者" in key):
            if "作者地区" not in key:
                book.setAuther(value.replace("作者: ", "").replace("编者: ", ""))
        elif ("定价:" in key) or ("定价：" in key):
            book.setFixPrice(value.replace("定价: ", "").replace("价格: ", ""))
        elif ("出版社" in key) or ("出版社" in key):
            book.setPress(value.replace("出版社名称:", ""))
    db.insert_book_data(book)
    db.update_item_url_status(1,item_id)
    print(detail_map)
    #转换成book 信息
    #保存
def run_other(adb):
    if adb.xpath("评价").exists:
        adb.xpath("评价").click()
        adb.swipe_ext("up", scale=0.8)  # 代码会vkk
        adb.swipe_ext("down", scale=0.5)  # 代码会vkk
    if adb.xpath("详情").exists:
        adb.xpath("详情").click()
        adb.swipe_ext("up", scale=0.8)  # 代码会vkk
        adb.swipe_ext("down", scale=0.8)  # 代码会vkk
    # if adb.xpath("客服").exists:
    #     adb.xpath("客服").click()
    #     adb.press("back")

def run(adbNum,items):
    if items is None or len(items) == 0:
        return
    adb = u2.connect(adbNum)  # connect to device
    adb.app_start("com.taobao.taobao")
    for item in items:
        #检查是否再首页,不在首页需要退回首页
        while True:
            if adb.xpath("首页").exists is False:
                #不存在需要退回首页
                adb.press("back")
            else:
                break
        adb.xpath("扫一扫").parent().click()
        adb.send_keys(item.get("item_url"))
        adb.xpath("搜索").click()
        #判断商品是否存在
        exist = adb.xpath("商品过期不存在").wait(timeout=1)
        exist2 = adb.xpath("宝贝不在了").wait(timeout=1)
        if exist is not None or exist2 is not None:
            log.info("商品%s过期或不存在", )
            return "商品%s过期或不存在".format(item)
        time.sleep(1)
        while True:
            adb.swipe_ext("up", scale=0.8)  # 代码会vkk
            time.sleep(1)
            xpath = adb.xpath("参数").exists
            if xpath is True:
                break
        adb.xpath("参数").click()
        detail_map = {}
        while True:
            container = adb.xpath("@com.taobao.taobao:id/container").all()
            for con in container:
                childs = con.elem.getchildren()
                if len(childs) < 2:
                    continue
                key=""
                value=""
                for childEle in childs:
                   if childEle.get("resource-id") == 'com.taobao.taobao:id/name' :
                       key = childEle.get("text")
                   if childEle.get("resource-id") == 'com.taobao.taobao:id/value':
                       value = childEle.get("text")
                detail_map.setdefault(key,value)
            if detail_map.get("出版社名称") is None:
                adb.swipe_ext("up", scale=0.8)  # 代码会vkk
                time.sleep(0.5)
            else:
                break
        adb.press("back")
        #转换信息并保存
        conver_save_book_info(item,detail_map)
        #执行其他操作
        run_other(adb)
if __name__ == '__main__':
    # items=[
    #     "http://detail.tmall.com/item.htm?id=16879965222&rn=c168cf9aa8b1132db15ae0e95ea2add1",
    #     "http://detail.tmall.com/item.htm?id=610461213303&rn=a8827a4b5c3e98090d7e73d0e88b2940&abbucket=14",
    #     "http://detail.tmall.com/item.htm?id=525693852629&rn=0e0537a6237d9d812a724d577ac11629&abbucket=14",
    # ]
    # run("e574eade",items)
    itemUrls = db.get_book_url_by_status(0)
    run("e574eade",itemUrls)

