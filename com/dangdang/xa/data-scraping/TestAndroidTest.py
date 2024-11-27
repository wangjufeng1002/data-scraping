import uiautomator2 as u2
from adbutils import adb
import json, re, demjson
import json
import multiprocessing
import os
import random
import re
import threading
import time
import traceback
def adb_list():
    for d in adb.device_list():
        print(d.serial)  # print device serial

    d = adb.device(serial="98957931")

    # or
    d = adb.device(transport_id=24)  # transport_id can be found in: adb devices -l

    # You do not need to offer serial if only one device connected
    # RuntimeError will be raised if multi device connected
    d = adb.device()





def click_search(devices, name,port, phone):
    devices.xpath('//*[@content-desc="搜索栏"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]').click()
    devices.send_keys("双节棍")
    devices.xpath("搜索").click()

def go_back_home(device):
    print(" go_back_home start")
    while device.xpath("推荐").exists is False or device.xpath("扫一扫").exists is False or device.xpath(
            "搜索").exists is False:
        if device.xpath("首页").exists is True:
            device.xpath("首页").click()
        else:
            go_back(device, 1)
            device.xpath("首页").wait(timeout=0.1)
    print(" go_back_home end")
def go_back(devices, times):
    print(" go_back start ")
    for i in range(times):
        devices.press("back")
    print(" go_back end ")

# 获取搜索按钮坐标
def get_search_button(devices):
    return devices.xpath('@com.taobao.taobao:id/searchbtn')
# 获取搜索框坐标
def get_search_view(devices):
    return devices.xpath('@com.taobao.taobao:id/sv_search_view').child('/android.widget.FrameLayout')


if __name__ == '__main__':
    d = u2.connect_usb("98957931")
    # app_list = d.app_list()
    # print(app_list)
    # d.app_stop("com.taobao.taobao")
    # # d_app_list = d.app_list()
    # d.app_start("com.taobao.taobao")

    click_search(d,"双节棍","98957931",True)
    #adb_list()
