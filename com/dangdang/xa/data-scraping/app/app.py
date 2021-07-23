import uiautomator2 as u2
import time
import subprocess
import db
import math
import multiprocessing
import threading
import re
import entity

file_object = open('../TM/result.txt', "a", encoding='utf-8')
last_date = ''


def run_cmd(cmd):
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    pr.wait()
    out = pr.stdout.readlines()
    return out


def kill_adb_connect():
    cmd = r'adb kill-server'
    run_cmd(cmd)
    print("断开所有连接")


def restart_memu(i):
    cmd = r'memuc isvmrunning -i ' + str(i)
    out = run_cmd(cmd)[0]
    if "Not" in str(out):
        cmd = r'memuc start -i ' + str(i)
    else:
        cmd = r'memuc reboot -i ' + str(i)
    out = run_cmd(cmd)[0]
    print('模拟器' + str(i) + str(out))


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
    get_search_view(devices).click_exists(timeout=10)
    time.sleep(0.5)
    devices.set_fastinput_ime(True)
    time.sleep(0.5)
    devices.send_keys(name)
    time.sleep(0.5)
    get_search_button(devices).click_exists(timeout=10)


def get_item_detail(item_id, devices):
    devices.xpath('@com.taobao.taobao:id/uik_public_menu_action_icon').wait()
    content = ''
    page_item = devices.xpath('@com.taobao.taobao:id/mainpage').child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    parseAppText(item_id, content)
    return content


def login(devices):
    devices.xpath("我的淘宝").click()
    devices.xpath("设置").click_exists(timeout=30)
    time.sleep(1)
    devices.xpath("退出登录").click()
    time.sleep(1)
    devices.xpath("退出当前账户").click()
    time.sleep(1)
    devices.xpath("更多").click()
    time.sleep(1)
    devices.xpath("换个账户登录").click()
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_account_et").set_text("superamayamay")
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_next_btn").click()
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_password_et").set_text("ztv963852_QWE")
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_next_btn").click()
    time.sleep(1)
    devices.set_fastinput_ime(False)


def skip(devices):
    while True:
        skip_update(devices)
        skip_hongbao(devices)
        skip_positive(devices)
        time.sleep(1)


def process(device, list):
    d = u2.connect(device)
    d.app_stop("com.taobao.taobao")
    time.sleep(1)
    d.app_start("com.taobao.taobao")
    threading.Thread(target=skip, args=(d,)).start()
    time.sleep(1)
    d.xpath('@com.taobao.taobao:id/searchbtn').wait()
    get_search_view(d).click_exists(timeout=10)
    d.press("back")
    for data in list:
        click_search(d, data['item_url'])
        time.sleep(1)
        valid_button = valid(d)
        if valid_button is not None:
            # 跳转换号登录
            print("账号暂时失效")
            time.sleep(1)
            go_back(d, 4)
            login(d)
        get_item_detail(devices=d, item_id=data['item_id'])
        time.sleep(1)
        go_back(d, 3)


def go_back(devices, times):
    for i in range(times):
        devices.press("back")
        time.sleep(0.3)


def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def skip_positive(devices):
    button = devices.xpath('@com.taobao.taobao:id/provision_positive_button').wait(3)
    if button is not None:
        button.click()


def parseAppText(item_id, text):
    text = text.replace("||", " ")
    info = entity.AppBookInfo(itemId=item_id, defaultPrice=None, activePrice=None, coupons=None, free=None, sales=None,
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
        info.sales = groups
    match = re.search(u"月销(.+?)\d+", text)
    if match is not None:
        groups = match.group(0)
        info.sales = groups

    if len(coupons) > 0:
        info.coupons = (",".join(coupons))
    db.update_info(info)
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


def init_memu(n):
    for i in range(n):
        restart_memu(i)


def valid(device):
    return device.xpath('@android:id/decor_content_parent').wait(timeout=1)


def skip_hongbao(devices):
    hongbao = devices.xpath("@com.taobao.taobao:id/layermanager_penetrate_webview_container_id").child(
        "//android.widget.ImageView").all()
    if len(hongbao) > 0:
        hongbao[1].click()


def skip_update(devices):
    update = devices.xpath("立即下载").wait(1)
    if update is not None:
        devices.xpath("取消").click()


# com.taobao.taobao
if __name__ == '__main__':
    while True:
        init_memu(1)
        time.sleep(5)
        devices_list = get_phone_list()
        data = db.get_need_process()
        if len(data) == 0:
            break
        lists = list_split(data, math.ceil(len(data) / len(devices_list)))
        threads = []
        for index, device in enumerate(devices_list):
            p = multiprocessing.Process(target=process, args=(device, lists[index]))
            threads.append(p)
            p.start()
        for t in threads:
            t.join()
        kill_adb_connect()
