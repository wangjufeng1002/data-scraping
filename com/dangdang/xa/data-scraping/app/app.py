import random

import uiautomator2 as u2
import time
import subprocess
import db
import math
import multiprocessing
import threading
import re
import entity
import MyLog
from timeit import default_timer
import datetime

file_object = open('../TM/result.txt', "a", encoding='utf-8')
main_end = False
log = MyLog.Logger('ha').get_log()


def run_cmd(cmd):
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    pr.wait()
    out = pr.stdout.readlines()
    return out


def kill_adb_connect():
    cmd = r'adb kill-server'
    run_cmd(cmd)
    log.info("断开所有连接")


def restart_memu(i):
    cmd = r'memuc isvmrunning -i ' + str(i)
    out = run_cmd(cmd)[0]
    if "Not" in str(out):
        cmd = r'memuc start -i ' + str(i)
    else:
        cmd = r'memuc reboot -i ' + str(i)
    out = run_cmd(cmd)[0]
    log.info('模拟器' + str(i) + str(out))


def get_phone_list():  # 获取手机设备
    cmd = r'adb.exe devices'  # % apk_file
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    pr.wait()  # 不会马上返回输出的命令，需要等待
    out = pr.stdout.readlines()  # out = pr.stdout.read().decode("UTF-8")
    devices = []
    for i in (out)[1:-1]:
        device = str(i).split("\\")[0].split("'")[-1]
        devices.append(device)
    log.info("获取到的设备列表%s", devices)
    return devices  # 手机设备列表


def get_search_view(devices):
    return devices.xpath('@com.taobao.taobao:id/sv_search_view').child('/android.widget.FrameLayout')


def get_search_button(devices):
    return devices.xpath('@com.taobao.taobao:id/searchbtn')


# 查看评论
def random_comment(devices):
    devices.swipe_ext("up", scale=1)
    time.sleep(0.5)
    devices.swipe_ext("up", scale=0.6)
    time.sleep(0.5)
    comment=devices.xpath('查看全部').wait(timeout=1)
    if comment is not None:
        devices.xpath("查看全部").click()
        time.sleep(1)
        devices.swipe_ext("up", scale=0.7)
        go_back(devices, 1)


def random_search(devices):
    keys = ['卫生纸', '电脑', '华为', '联想', '洗衣液', '苹果', '显卡', '人间失格', '宇宙的琴弦', '圈量子理论', 'usb', '零食', '杯子', '袜子', '球衣', '嘉然',
            '七海', '康师傅', '辣条', '小熊饼干', '灯泡', '墙纸', 'python教学']
    get_search_view(devices).click_exists(timeout=10)
    time.sleep(0.5)
    devices.set_fastinput_ime(True)
    time.sleep(0.5)
    devices.send_keys(keys[random.randint(0, len(keys) - 1)])
    time.sleep(0.5)
    get_search_button(devices).click_exists(timeout=10)
    time.sleep(0.5)
    random_swipe(devices, False)
    time.sleep(1)
    go_back(devices, 3)


def click_search(devices, name):
    # 随机刷新
    random_refresh(devices)
    # 随机行为

    random_shop_cart(devices)
    random_message(devices)
    random_switch_tabs(devices)
    get_search_view(devices).click_exists(timeout=10)
    time.sleep(0.5)
    devices.set_fastinput_ime(True)
    time.sleep(0.5)
    devices.send_keys(name)
    time.sleep(0.5)
    get_search_button(devices).click_exists(timeout=10)


def random_swipe(devices, back):
    times = random.randint(1, 3)
    for i in range(0, times):
        devices.swipe_ext("up", scale=0.5)
    if back is True:
        for i in range(0, times):
            devices.swipe_ext("down", scale=0.5)


def random_refresh(devices):
    times = random.randint(0, 3)
    for i in range(0, times):
        time.sleep(0.2)
        devices.swipe_ext("down", scale=0.3)
    time.sleep(1)


# 随机行为 浏览购物车
def random_shop_cart(devices):
    do = random.randint(0, 1)
    if do == 1:
        devices.xpath("购物车").click()
        time.sleep(1)
        go_back(devices, 1)
        time.sleep(1)


# 随机行为 浏览消息
def random_message(devices):
    do = random.randint(0, 1)
    if do == 1:
        devices.xpath("消息").click()
        time.sleep(1)
        go_back(devices, 1)
        time.sleep(1)


# 随机行为 切换标签页面
def random_switch_tabs(devices):
    do = random.randint(0, 1)
    tabs = devices.xpath("//android.widget.HorizontalScrollView").child("//android.widget.TextView").all()
    if do == 1:
        index = random.randint(0, 3)
        tabs[index].click()
        time.sleep(1)


def get_item_detail(item_id, devices, account, index):
    exist=devices.xpath("商品过期不存在").wait(timeout=2)
    if exist is not None:
        log.info("商品%s过期或不存在",item_id)
        parseAppText(item_id, "商品过期或不存在")
        return
    devices.xpath('@com.taobao.taobao:id/uik_public_menu_action_icon').wait()
    content = ''
    page_item = devices.xpath('@com.taobao.taobao:id/mainpage').child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    parseAppText(item_id, content)
    log.info("进程%s账号%s,获取商品%s数据:%s", str(index), account, item_id, content)
    time.sleep(0.3)
    select = random.randint(0, 1)
    if select == 0:
        random_comment(devices)
    else:
        random_swipe(devices, False)
    time.sleep(1)
    return content


def login(devices):
    restart_app(devices)
    user = db.get_user()
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
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_account_et").set_text(user['account'])
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_next_btn").click()
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_password_et").set_text(user['password'])
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_next_btn").click()
    time.sleep(1)
    devices.set_fastinput_ime(False)
    time.sleep(1)
    devices.xpath("首页").click()
    return user


def skip(devices):
    while True:
        skip_update(devices)
        skip_hongbao(devices)
        skip_positive(devices)
        time.sleep(1)
        if main_end is True:
            break


def restart_app(devices):
    devices.app_stop("com.taobao.taobao")
    time.sleep(1)
    devices.app_start("com.taobao.taobao")


def process(device, list, index):
    start = default_timer()
    global main_end
    main_end = False
    logged_account=''
    try:
        d = u2.connect(device)
    except:
        log.info("线程%s连接adb发生错误,重启app",index)
        restart_memu(index)

    try:
        restart_app(d)
        t = threading.Thread(target=skip, args=(d,))
        t.start()
        time.sleep(1)
        logged_account = get_logged_account(d)
        log.info("进程%s登录的账号是%s", str(index), logged_account)
        d.xpath('@com.taobao.taobao:id/searchbtn').wait()
        get_search_view(d).click_exists(timeout=10)
        go_back(d, 3)
    except:
        main_end=False
    for data in list:
        try:
            n = random.randint(0, 8)
            if n == 4:
                random_search(d)
            sleep = random.randint(3, 20)
            time.sleep(sleep)
            log.info("进程%s,账号%s,休息%s秒", index, logged_account, sleep)
            click_search(d, data['item_url'])
            time.sleep(1)
            valid_button = valid(d)
            if valid_button is not None:
                # 跳转换号登录
                log.info("进程%s账号%s暂时失效", index, logged_account)
                time.sleep(1)
                go_back(d, 4)
                logged_account = login(d)['account']
                account_info = db.get_account_info(logged_account)
                if int(account_info['fail_times']) > 5:
                    log.info("账号%s,出现滑块次数过多,程序休息10分钟")
                    time.sleep(360)
                log.info("进程%s切换账号登录%s", str(index), logged_account)
                continue
            get_item_detail(devices=d, item_id=data['item_id'], account=logged_account, index=index)
            time.sleep(1)
            go_back(d, 3)
        except Exception as e:
            log.info("进程%s,商品%s抓取发生异常,重启app,%s",index,data,e)
            restart_app(d)
            continue
    main_end = True
    log.info("进程%s账号%s,抓取数据%s个,用时%s", str(index), logged_account, str(len(list)), str(default_timer() - start))


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
                              originalText=text,name=None)
    coupons = []
    text = text[3:]
    # 先替换掉日期影响
    month = datetime.datetime.now().month
    match = re.search(str(month) + "月" + "(.+?)开卖", text)
    if match is not None:
        groups = match.group(0)
        text = text.replace(groups, "日期替换")
    # 活动价格
    match = re.search("￥(.+?)[\d.]+", text)
    if match is not None:
        groups = match.group(0)
        if groups is not None:
            search = re.search("\d(\d)*[\d.]*", groups)
            if search is not None:
                price = search.group(0)
                # 都赋值，后面价格定位替换
                info.activePrice = price
                info.defaultPrice = price
            else:
                info.activePrice = groups
                info.defaultPrice = groups
    # 券后价
    match = re.search("(券后|折后)￥(.+?)[\d.]+", text)
    if match is not None:
        groups = match.group(0)
        if groups is not None:
            search = re.search("\d(\d)*[\d.]*", groups)
            if search is not None:
                price = search.group(0)
                info.activePrice = price
            else:
                info.activePrice = groups
    match = re.search("价格￥(.+?)[\d.]+", text)
    if match != None:
        groups = match.group(0)
        if groups is not None:
            search = re.search("\d(\d)*[\d.]*", groups)
            if search is not None:
                price = search.group(0)
                info.defaultPrice = price
            else:
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

    #提取名称
    if "큚" in text and "ꄪ" not  in text:
        match = re.search(u"큚(.+?)+", text)
    else:
        match = re.search(u"큚(.+?)ꄪ", text)
    if match != None:
        groups = match.group(0)
        ignoTextGroups = re.search(u"큚(.+?)领取", groups)
        if ignoTextGroups != None:
            groups = groups.replace(ignoTextGroups.group(0), "")
        groups = groups.replace(" ", "").replace("큚", "").replace("ꄪ", "")
        info.name = groups
    if len(coupons) > 0:
        info.coupons = (",".join(coupons))
    print(info.toString())
    db.update_info(info)
    file_object.write(info.toString() + "\n")
    file_object.flush()

def init_memu(n):
    for i in range(n):
        restart_memu(i)


def valid(devices):
    return devices.xpath('@android:id/decor_content_parent').wait(timeout=2)


def skip_hongbao(devices):
    hongbao = devices.xpath("@com.taobao.taobao:id/layermanager_penetrate_webview_container_id").child(
        "//android.widget.ImageView").all()
    if len(hongbao) > 0:
        hongbao[1].click()


def skip_update(devices):
    update = devices.xpath("立即下载").wait(1)
    if update is not None:
        devices.xpath("取消").click()


def get_logged_account(devices):
    devices.xpath("我的淘宝").click()
    devices.xpath("设置").click_exists(timeout=30)
    time.sleep(1)
    user_nick = devices.xpath("@com.taobao.taobao:id/tv_setting_page_user_nick").wait(timeout=3)
    devices.press("back")
    time.sleep(0.3)
    devices.xpath("首页").click()
    return user_nick.text


# com.taobao.taobao
if __name__ == '__main__':
    d=u2.connect()
    get_item_detail("12",d,"123",1)
    # count = input("请输入模拟器个数")
    # while True:
    #     init_memu(int(count))
    #     time.sleep(5)
    #     devices_list = get_phone_list()
    #     data = db.get_need_process()
    #     if len(data) == 0:
    #         break
    #     lists = list_split(data, math.ceil(len(data) / len(devices_list)))
    #     threads = []
    #     for index, device in enumerate(devices_list):
    #         p = multiprocessing.Process(target=process, args=(device, lists[index], index))
    #         threads.append(p)
    #         p.start()
    #     for t in threads:
    #         t.join()
    #     kill_adb_connect()
