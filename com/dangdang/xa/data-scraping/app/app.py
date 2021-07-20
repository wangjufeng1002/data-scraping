import uiautomator2 as u2
import time
import subprocess
import db
import math
import multiprocessing
import  re
import os
import cv2
import entity


def get_item(devices):
    items = devices(className="android.support.v7.widget.RecyclerView",
                    resourceId="com.taobao.taobao:id/libsf_srp_header_list_recycler").child(
        className="android.widget.LinearLayout")
    index = 0
    while index < items.count:
        items[index].click()
        time.sleep(0.5)
        get_item_detail(devices)
        devices.press("back")
        index += 3


def get_phone_list():  # 获取手机设备
    cmd = r'D:\adb.exe devices'  # % apk_file
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    pr.wait()  # 不会马上返回输出的命令，需要等待
    out = pr.stdout.readlines()  # out = pr.stdout.read().decode("UTF-8")
    devices = []
    for i in (out)[1:-1]:
        device = str(i).split("\\")[0].split("'")[-1]
        devices.append(device)
    print(devices)
    return devices  # 手机设备列表


def get_buy_content(devices):
    page_item = devices(className="android.widget.LinearLayout",
                        resourceId="com.taobao.taobao:id/ll_bottom_bar").child()
    for item in page_item:
        print(item.info)


def click_search(devices, name):
    devices.set_fastinput_ime(True)
    devices.click(300, 150)
    time.sleep(1)
    devices.send_keys(name)
    devices.send_action("search")


def get_item_detail(devices):
    content = ''
    page_item = devices.xpath('@com.taobao.taobao:id/mainpage').child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    parseAppText(content)
    return content


def process(deivce, list):
    d = u2.connect(deivce)
    for data in list:
        click_search(d, data['item_url'])
        time.sleep(1)
        get_item_detail(devices=d)
        time.sleep(1)
        d.press("back")
        time.sleep(0.3)
        d.press("back")
        time.sleep(0.3)
        d.press("back")
        time.sleep(0.3)


def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]

def parseAppText(text):
    info = entity.AppBookInfo(itemId=None,defaultPrice= None,activePrice= None,coupons= None,free= None)
    coupons = []
    text = text[3:]
    # 活动价格
    match = re.search("^(.+?)[\d.]+", text)
    if match != None:
        # 领券内容
        groups = match.group(0)
        #都赋值，后面价格定位替换
        info.activePrice = groups
        info.defaultPrice = groups
    # 券后价
    match = re.search("券后(.+?)[\d.]+", text)
    if match != None:
        groups = match.group(0)
        info.activePrice = groups
    match = re.search("价格(.+?)[\d.]+", text)
    if match != None:
        groups = match.group(0)
        info.defaultPrice = groups
    #提取 “领券...领取” 中的内容
    match = re.search("领券(.+?)领取", text)
    if match != None:
        groups = match.group(0)
        coupons.append(groups)
    # 提取 “查看...领取” 中的内容
    match = re.search("查看(.+?)领取", text)
    if match != None:
        # 领券内容
        groups = match.group(0)
        coupons.append(groups)
    #满减
    match = re.search("满(.+?)减(.+?)\d+", text)
    if match != None:
        groups = match.group(0)
        coupons.append(groups)
        #print(groups)
        # 包邮
    match = re.search("满(\d+?)享包邮", text)
    if match != None:
        groups = match.group(0)
        # print(groups)
        info.free=groups
    if len(coupons) >0:
        info.coupons = (",".join(coupons))
    print(info.toString())
        # 包邮
    #销量
    # match = re.search(u"月销(.+?)(\+|\d+)", text)
    # if match != None:
    #     groups = match.group(0)
    #     constants.append(groups)
        #print(groups)

    #print(splits)
# com.taobao.taobao
if __name__ == '__main__':
    devices_list = get_phone_list()
    data = db.get_need_process()
    lists = list_split(data, math.ceil(len(data)/len(devices_list)))
    for index, device in enumerate(devices_list):
        p = multiprocessing.Process(target=process, args=(device, lists[index]))
        p.start()
