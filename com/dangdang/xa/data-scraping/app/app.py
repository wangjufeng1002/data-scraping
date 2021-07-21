import uiautomator2 as u2
import time
import subprocess
import db
import math
import multiprocessing
import re
import entity

file_object = open('../TM/result.txt', "a", encoding='utf-8')


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


def get_search_view(devices):
    return devices.xpath('@com.taobao.taobao:id/sv_search_view').child('/android.widget.FrameLayout')


def get_search_button(devices):
    return devices.xpath('@com.taobao.taobao:id/searchbtn')


def click_search(devices, name):
    devices.set_fastinput_ime(True)
    get_search_view(devices).click()
    time.sleep(0.5)
    devices.send_keys(name)
    time.sleep(0.5)
    get_search_button(devices).click()


def get_item_detail(item_id, devices):
    content = ''
    page_item = devices.xpath('@com.taobao.taobao:id/mainpage').child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    parseAppText(item_id, content)
    return content


def process(deivce, list):
    d = u2.connect(deivce)
    d.app_stop("com.taobao.taobao")
    time.sleep(1)
    d.app_start("com.taobao.taobao")
    time.sleep(1)
    for data in list:
        click_search(d, data['item_url'])
        time.sleep(1)
        get_item_detail(devices=d, item_id=data['item_id'])
        time.sleep(1)
        d.press("back")
        time.sleep(0.3)
        d.press("back")
        time.sleep(0.3)
        d.press("back")
        time.sleep(1)


def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def parseAppText(item_id, text):
    text = text.replace("||", " ")
    info = entity.AppBookInfo(itemId=item_id, defaultPrice=None, activePrice=None, coupons=None, free=None,sales=None,
                              originalText=text)
    coupons = []
    text = text[3:]
    # 活动价格
    match = re.search("^(.+?)[\d.]+", text)
    if match != None:
        # 领券内容
        groups = match.group(0)
        # 都赋值，后面价格定位替换
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
    # 提取 “领券...领取” 中的内容
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
    # 满减
    match = re.search("满(.+?)减(.+?)\d+", text)
    if match != None:
        groups = match.group(0)
        coupons.append(groups)
        # print(groups)
        # 包邮
    match = re.search("满(\d+?)享包邮", text)
    if match != None:
        groups = match.group(0)
        # print(groups)
        info.free = groups

    match = re.search(u"月销(.+?)\+", text)
    if match != None:
        groups = match.group(0)
        info.sales=groups
    match = re.search(u"月销(.+?)\d+", text)
    if match != None:
        groups = match.group(0)
        info.sales = groups

    if len(coupons) > 0:
        info.coupons = (",".join(coupons))
    print(info.toString())
    file_object.write(info.toString() + "\n")
    file_object.flush()
    # 包邮
    # 销量
    # match = re.search(u"月销(.+?)(\+|\d+)", text)
    # if match != None:
    #     groups = match.group(0)
    #     constants.append(groups)
    # print(groups)

    # print(splits)


# com.taobao.taobao
if __name__ == '__main__':
    devices_list = get_phone_list()
    while True:
        data = db.get_need_process()
        if len(data) == 0:
            break
        db.update_status(data)
        lists = list_split(data, math.ceil(len(data) / len(devices_list)))
        threads = []
        for index, device in enumerate(devices_list):
            p = multiprocessing.Process(target=process, args=(device, lists[index]))
            threads.append(p)
            p.start()
        for t in threads:
            t.join()
