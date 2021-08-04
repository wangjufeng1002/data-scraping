import json
import random
import traceback

import requests
import uiautomator2 as u2
import time
import subprocess
import multiprocessing
import threading
import MyLog
from timeit import default_timer
from multiprocessing import Manager
import db
import socket

main_end = False
restart_app = False
log = MyLog.Logger('CMT').get_log()


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def run_cmd(cmd):
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    pr.wait()
    out = pr.stdout.readlines()
    return out


def kill_adb_connect():
    cmd = r'adb kill-server'
    run_cmd(cmd)
    log.info("断开所有连接")


def get_memu_status(number):
    cmd = r'memuc isvmrunning -i ' + str(number)
    out = run_cmd(cmd)[0]
    if "Not" in str(out):
        return False
    else:
        return True


def stop_memu(i):
    cmd = r'memuc stop -i ' + str(i)
    run_cmd(cmd)


def restart_memu(i):
    global restart_app
    restart_app = True
    cmd = r'memuc isvmrunning -i ' + str(i)
    out = run_cmd(cmd)[0]
    if "Not" in str(out):
        cmd = r'memuc start -i ' + str(i)
    else:
        cmd = r'memuc reboot -i ' + str(i)
    out = run_cmd(cmd)[0]
    log.info('模拟器' + str(i) + str(out))
    restart_app = False


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
def random_comment(devices, weight):
    if random_do(int(weight) * 10):
        log.info("随机策略查看评论")
        devices.swipe_ext("up", scale=1)
        time.sleep(0.5)
        devices.swipe_ext("up", scale=0.6)
        time.sleep(0.5)
        comment = devices.xpath('查看全部').wait(timeout=1)
        if comment is not None:
            devices.xpath("查看全部").click()
            time.sleep(1)
            devices.swipe_ext("up", scale=0.7)
            go_back(devices, 1)


def random_search(devices):
    keys = ['卫生纸', '电脑', '华为', '联想', '洗衣液', '苹果', '显卡', '人间失格', '宇宙的琴弦', '圈量子理论', 'usb', '零食', '杯子', '袜子', '球衣', '嘉然',
            '七海', '康师傅', '辣条', '小熊饼干', '灯泡', '墙纸', 'python教学', '阿迪', '耐克', '背包', '甜品', '面具', '玩具', 'lovelive']
    get_search_view(devices).click_exists(timeout=2)
    time.sleep(0.5)
    get_search_view(devices).click_exists(timeout=5)
    time.sleep(0.5)
    devices.set_fastinput_ime(True)
    time.sleep(0.5)
    devices.send_keys(keys[random.randint(0, len(keys) - 1)])
    time.sleep(0.5)
    get_search_button(devices).click_exists(timeout=10)
    if valid(devices) is not None:
        log.info("随机搜索出现验证")
        time.sleep(1)
        go_back(devices, 4)
        return
    time.sleep(0.5)
    random_swipe(devices, False)
    time.sleep(1)
    go_back(devices, 3)


def click_search(devices, name, random_policy):
    # 随机策略
    random_refresh(devices, random_policy['refresh'])
    random_shop_cart(devices, random_policy['shopCart'])
    random_message(devices, random_policy['message'])
    random_switch_tabs(devices, random_policy['switchTabs'])
    get_search_view(devices).click_exists(timeout=10)
    time.sleep(0.5)
    # 点击一下空白处 让pre search 弹窗消失
    devices.click(300, 300)
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


def random_do(weight):
    number = random.randint(0, 10)
    if number < weight:
        return True
    return False


def random_refresh(devices, weight):
    if random_do(int(weight) * 10):
        log.info("随机策略刷新")
        time.sleep(0.2)
        devices.swipe_ext("down", scale=0.3)
        time.sleep(1)


# 随机行为 浏览购物车
def random_shop_cart(devices, weight):
    if random_do(int(weight) * 10):
        log.info("随机策略查看购物车")
        devices.xpath("购物车").click()
        time.sleep(1)
        go_back(devices, 1)
        time.sleep(1)


# 随机行为 浏览消息
def random_message(devices, weight):
    if random_do(int(weight) * 10):
        log.info("随机策略查看消息")
        devices.xpath("消息").click()
        time.sleep(1)
        go_back(devices, 1)
        time.sleep(1)


# 随机行为 切换标签页面
def random_switch_tabs(devices, weight):
    if random_do(int(weight) * 10):
        log.info("随机策略切换tabs")
        tabs = devices.xpath("//android.widget.HorizontalScrollView").child("//android.widget.TextView").all()
        index = random.randint(0, 3)
        tabs[index].click()
        time.sleep(1)


def get_item_detail(item_id, devices, account, index, conf):
    exist = devices.xpath("商品过期不存在").wait(timeout=2)
    if exist is not None:
        log.info("商品%s过期或不存在", item_id)
        return
    devices.xpath('@com.taobao.taobao:id/uik_public_menu_action_icon').wait()
    content = ''
    page_item = devices.xpath('@com.taobao.taobao:id/mainpage').child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    log.info("进程%s账号%s,获取商品%s数据:%s", str(index), account, item_id, content)
    time.sleep(0.3)
    random_comment(devices, conf['comment'])

    time.sleep(1)
    return content


def login(devices, account, password):
    restart_app(devices)
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
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_account_et").set_text(account)
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_next_btn").click()
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_password_et").set_text(password)
    time.sleep(1)
    devices.xpath("@com.taobao.taobao:id/aliuser_recommend_login_next_btn").click()
    time.sleep(1)
    devices.set_fastinput_ime(False)
    time.sleep(1)
    devices.xpath("首页").click()


def skip(devices):
    start_time = default_timer()
    while True:
        skip_update(devices)
        skip_hongbao(devices)
        skip_positive(devices)
        time.sleep(1)
        # 开启3分钟 线程退出 防止主线程意外关闭而这个线程还没结束
        if default_timer() - start_time > 120:
            break
        if main_end is True:
            break


def restart_app(devices):
    devices.app_stop("com.taobao.taobao")
    time.sleep(1)
    devices.app_start("com.taobao.taobao")


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


def get_memu_config():
    with open("./conf.json", "r+", encoding='utf-8') as f:
        conf_text = f.read()
        return json.loads(conf_text)


def get_memu_port(number):
    ports = get_memu_config().get("accountInfo")
    for port in ports:
        if port['number'] == number:
            return port['port']
    return None


def get_memu_login_account(number):
    accountInfo = get_memu_config().get("accountInfo")
    for account in accountInfo:
        if account['number'] == number:
            return str(account['account'])
    return None


def get_memu_policy(account):
    data = db.get_job_status_by_account(account)
    config = json.loads(data['config'])
    log.info("获得账号配置信息:%s", config)
    return config['random']


def process_data(number, account, passwd, products, port):
    log.info("开始处理数据,入参:account:%s,passwd:%s,number:%s,products:%s", account, passwd, number, products)
    ip = get_host_ip()
    job_status = db.get_job_status(ip, port)
    if job_status['run_status'] == 1:
        log.info("ip:%s,port:%s的分片正在运行,请稍后请求", ip, port)
        return -1
    # 更新为运行状态
    db.update_job_status(ip, port, '1')
    if restart_app is True:
        log.info("正在启动app,请稍后重试")
        return -1
    try:
        status = get_memu_status(number)
        if status is False:
            restart_memu(number)
        devices_addr = '127.0.0.1:' + str(port)
        p = multiprocessing.Process(target=run, args=(devices_addr, number, account, passwd, products))
        p.start()

        p.join()
        db.update_job_status(ip, port, '0')
    except Exception as e:
        log.info(traceback.format_exc())
        db.update_job_status(ip, port, '0')


def heart(number):
    try:
        log.info("心跳检测,number:%s", number)
        port = get_memu_port(number)
        if port is None:
            log.info("获取配置端口号失败,请检查配置")
            return
        devices_addr = '127.0.0.1:' + port
        device = u2.connect(devices_addr)
        device.xpath("我的淘宝").click_exists(timeout=5)
        time.sleep(1)
        device.xpath("设置").click_exists(timeout=5)
        time.sleep(1)
        device.press("back")
        log.info("app运行正常")
    except Exception as e:
        log.info("心跳监控APP出现异常,重启", e)
        restart_memu(number)


def run(devices_addr, number, account, password, products):
    try:
        global main_end
        main_end = False
        device = u2.connect(devices_addr)
        time.sleep(2)
        random_policy = get_memu_policy(account)
        device.app_start("com.taobao.taobao")
        # 开启跳过广告线程
        threading.Thread(target=skip, args=(device,)).start()
        logged_account = get_memu_login_account(number)
        log.info("当前模拟器登录的账号是:%s", logged_account)
        time.sleep(0.3)
        device.xpath("首页").click_exists(timeout=5)
        time.sleep(0.3)
        if account != logged_account:
            log.info("当前模拟器登录账号不一致,重新登录")
            login(device, account, password)
        for item in products:
            url = 'http://detail.tmall.com/item.htm?id=' + str(item)
            click_search(device, url, random_policy)
            time.sleep(1)
            valid_button = valid(device)
            if valid_button is not None:
                log.info("进程%s账号%s暂时失效", number, logged_account)
                db.update_account_info(account)
                # 账号失效了就暂时不用了,这次请求直接结束
                break
            content = get_item_detail(devices=device, item_id=item, account=logged_account, index=number,
                                      conf=random_policy)
            db.update_info(content, item)
            time.sleep(1)
            go_back(device, 3)
            start = random_policy['timeSleep']['begin']
            end = random_policy['timeSleep']['end']
            sleep_time = random.randint(int(start), int(end))
            time.sleep(sleep_time)
            log.info("账号%s休息%s秒", account, sleep_time)

        main_end = True
    except Exception as e:
        log.info(traceback.format_exc())
        main_end = True
        # 出现异常终止操作 并终止app
        stop_memu(number)
