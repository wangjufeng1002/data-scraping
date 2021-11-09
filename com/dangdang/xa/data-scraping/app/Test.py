import uiautomator2 as u2
import time
import os
import db
import requests
import json


def screeon(adb):
    adb.press("back")
    adb.swipe_ext("up", scale=0.9)
    return True


def open_app(adb):
    adb.app_start("com.taobao.taobao")


def check(d: u2.Device):
    print("出现验证码")
    xpath = d.xpath("@android:id/decor_content_parent")
    time.sleep(20)


def go_back_home(device):
    if device.xpath("首页").exists is True:
        device.xpath("首页").click()
    while device.xpath("首页").exists is False or device.xpath("扫一扫").exists is False or device.xpath(
            "搜索").exists is False:
        device.press("back")
        device.xpath("首页").wait(timeout=0.1)


import app_v2

if __name__ == '__main__':
    # adb = u2.connect("401fab3")
    # adb.app_start("com.taobao.taobao")
    # adb.xpath("扫一扫").parent().click()
    # adb.send_keys("http://detail.tmall.com/item.htm?id=642701262486")
    # adb.send_keys("https://detail.m.tmall.com/templatesNew/index?id=650554143519")
    # adb.send_keys("http://detail.tmall.com/item.htm?id=650554143519")
    # print(adb.xpath("很抱歉，您查看的宝贝不存在，可能已下架或被转移").exists)
    # os_open = os.open(r'.\pid\\' + "1.txt", os.O_CREAT | os.O_EXCL | os.O_RDWR)
    # os.write(os_open,str(1111).encode('UTF-8'))
    # os.remove(r'.\pid\\' + "1.txt")

    # exist = adb.xpath("商品过期不存在").wait(timeout=1)
    # exist2 = adb.xpath("宝贝不在了").wait(timeout=1)
    # if exist is not None or exist2 is not None:
    #     print("商品%s过期或不存在")
    # print(adb.app_current().get('package'))
    # print(adb.app_info("com.taobao.taobao"))
    # print(adb.app_list_running())
    # adb.watcher("首页").when("赚金币").call(lambda d:screeon(adb))
    # adb.watcher.start(1)
    # adb.watcher("1").when("信息").when("拨号").when("浏览器").when("相机").call(lambda d:open_app(adb))

    # adb.watcher("check").when("@android:id/decor_content_parent").call(lambda d:check(adb))
    # adb.watcher("goldCoins").when("赚金币").press("back")
    # adb.watcher.start(5)
    # time.sleep(20000)
    # time.sleep(20000)
    # screen = adb.info
    # if screen["screenOn"] == False:  # 屏幕状态
    #     adb.press("power")
    #     adb.swipe_ext("up", scale=0.9)
    #     print("灭屏状态")
    # elif screen["screenOn"] == True:  # 屏幕状态
    #     adb.swipe_ext("up", scale=0.9)
    #     print("亮屏状态")
    # if adb.xpath('//*[@resource-id="com.taobao.taobao:id/searchbtn"]').exists is False:
    #      adb.press("back")
    # running = adb.app_list_running()
    # adb.app_stop("com.taobao.taobao")
    # adb.app_start("com.taobao.taobao")

    # print(running)
    # adb.xpath("@nc_1_n1t").long_click()
    # adb.swipe_ext("right", scale=0.9)
    # adb.xpath(
    #     '//*[@resource-id="com.taobao.taobao:id/sv_search_view"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[5]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]').click()
    # adb.send_keys("哈哈")
    # adb.swipe_points([(165,1356),(945,1470)],0.09)
    # if adb.xpath("nc_1_refresh1").exists is True:
    #     adb.xpath("nc_1_refresh1").click()
    # view__all=  adb.xpath("@com.taobao.taobao:id/rv_main_container").child("//android.widget.HorizontalScrollView").child("//android.widget.TextView").all()
    # for tab in view__all:
    #     print(tab.text)
    # lock = db.update_job_status_lock("192.168.49.182", "21643", 1)

    # lock  = db.update_job_pid("192.168.49.182", "21643", 1)
    # print(lock)
    # get = requests.get("http://localhost:10003/product/getTaskData?port=%s".format("123456"))
    # json = json.loads(get.text)
    # print(json['taskId'])
    # print(json['taskLabel'])
    # print(json['itemIds

    # http://detail.tmall.com/item.htm?id=652135388183
    # http://detail.tmall.com/item.htm?id=626285676217
    # http://detail.tmall.com/item.htm?id=526553709162
    # http://detail.tmall.com/item.htm?id=565480423538
    device = u2.connect("7be1f4a9")
    #go_back_home(device)
    if device.xpath("@com.taobao.taobao:id/edit_del_btn").exists is True:
        device.xpath("@com.taobao.taobao:id/edit_del_btn").click()
        device.xpath("@com.taobao.taobao:id/searchEdit").click()
        device.send_keys("http://detail.tmall.com/item.htm?id=565480423538")
        device.xpath("搜索").click()
    detail = app_v2.get_item_detail(item_id="526553709162", devices=device, account='xxx', phone=True, sku=None)
    device.press("back")
    if device.xpath("网络竟然崩溃了").exists is True:
        device.xpath("刷新").click()
    if device.xpath("浮层关闭按钮").exists is True:
        print("定位到了")
        device.xpath("浮层关闭按钮").click()

# dict = dict()
# dict['1111']= 1
# dict['1111'] = 2
# print(dict)
