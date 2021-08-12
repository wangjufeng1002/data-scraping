import json
import random
import traceback

import uiautomator2 as u2
import time
import subprocess
import multiprocessing
import threading
import MyLog
from timeit import default_timer
import db
import socket
import timeout_decorator

# 主线程运行标志,来让跳过弹窗的子线程能随主线程终止而结束
main_end = False

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


@timeout_decorator.timeout(60)
def time_out_connect(addr):
    return u2.connect(addr)
def stop_memu(i):
    cmd = r'memuc stop -i ' + str(i)
    run_cmd(cmd)


def restart_memu(i, ip, port):
    db.update_job_status(ip, port, '2')
    cmd = r'memuc isvmrunning -i ' + str(i)
    out = run_cmd(cmd)[0]
    if "Not" in str(out):
        cmd = r'memuc start -i ' + str(i)
    else:
        cmd = r'memuc reboot -i ' + str(i)
    out = run_cmd(cmd)[0]
    log.info('模拟器' + str(i) + str(out))
    db.update_job_status(ip, port, '1')


def get_search_view(devices):
    return devices.xpath('@com.taobao.taobao:id/sv_search_view').child('/android.widget.FrameLayout')


def get_search_button(devices):
    return devices.xpath('@com.taobao.taobao:id/searchbtn')


# 查看评论
def random_comment(devices, weight, ip, port, account):
    if random_do(float(weight) * 10):
        db.insert_account_log(account, ip, port, "25", "账号随机查看评论")
        devices.swipe_ext("up", scale=1)
        time.sleep(0.5)
        devices.swipe_ext("up", scale=0.2)
        time.sleep(0.5)
        comment = devices.xpath('查看全部').wait(timeout=1)
        if comment is not None:
            devices.xpath("查看全部").click()
            time.sleep(1)
            devices.swipe_ext("up", scale=0.7)
            go_back(devices, 1)


def random_search(devices, random_policy, ip, port, account):
    if random_do(float(random_policy) * 10):
        db.insert_account_log(account, ip, port, "24", "账号随机搜索")
        keys = []
        words = db.get_keywords()
        for word in words:
            keys.append(word['key_words'])
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
            db.insert_account_log(account, ip, port, "-24", "账号随机搜索出现验证")
            time.sleep(1)
            go_back(devices, 4)
            return
        time.sleep(0.5)
        random_swipe(devices, False)
        time.sleep(1)
        go_back(devices, 3)


def click_search(devices, name, random_policy, ip, port, account):
    # 随机策略
    random_refresh(devices, random_policy['refresh'], ip, port, account)
    random_shop_cart(devices, random_policy['shopCart'], ip, port, account)
    random_message(devices, random_policy['message'], ip, port, account)
    random_switch_tabs(devices, random_policy['switchTabs'], ip, port, account)
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


def random_do(weight):
    number = random.randint(0, 10)
    if number < weight:
        return True
    return False


def random_refresh(devices, weight, ip, port, account):
    if random_do(float(weight) * 10):
        db.insert_account_log(account, ip, port, "20", "账号随机刷新")
        time.sleep(0.2)
        devices.swipe_ext("down", scale=0.3)
        time.sleep(1)


# 随机行为 浏览购物车
def random_shop_cart(devices, weight, ip, port, account):
    if random_do(float(weight) * 10):
        db.insert_account_log(account, ip, port, "21", "账号随机浏览购物车")
        devices.xpath("购物车").click()
        time.sleep(1)
        go_back(devices, 1)
        time.sleep(1)


# 随机行为 浏览消息
def random_message(devices, weight, ip, port, account):
    if random_do(float(weight) * 10):
        db.insert_account_log(account, ip, port, "22", "账号随机查看消息")
        devices.xpath("消息").click()
        time.sleep(1)
        go_back(devices, 1)
        time.sleep(1)


# 随机行为 切换标签页面
def random_switch_tabs(devices, weight, ip, port, account):
    if random_do(float(weight) * 10):
        db.insert_account_log(account, ip, port, "23", "账号随机切换标签页")
        tabs = devices.xpath("//android.widget.HorizontalScrollView").child("//android.widget.TextView").all()
        index = random.randint(0, 3)
        tabs[index].click()
        time.sleep(1)


def get_item_detail(item_id, devices, account, index, conf, ip, port):
    exist = devices.xpath("商品过期不存在").wait(timeout=2)
    if exist is not None:
        log.info("商品%s过期或不存在", item_id)
        return "商品%s过期或不存在".format(item_id)
    devices.xpath('@com.taobao.taobao:id/uik_public_menu_action_icon').wait()
    content = ''
    devices.swipe_ext("up", scale=0.5)
    page_item = devices.xpath('@com.taobao.taobao:id/mainpage').child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    log.info("进程%s账号%s,获取商品%s数据:%s", str(index), account, item_id, content)
    time.sleep(0.3)
    random_comment(devices, conf['comment'], ip, port, account)

    time.sleep(1)
    return content


def login(devices, account, password):
    restart_app_func(devices)
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


def restart_app_func(devices):
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


def get_memu_login_account(ip, port):
    job_info = db.get_job_status(ip, port)
    accountInfo = job_info['account']
    return accountInfo


def get_memu_policy(account):
    data = db.get_job_status_by_account(account)
    config = json.loads(data['config'])
    log.info("获得账号配置信息:%s", config)
    return config['random']


def process_data(account, passwd, products, port, task_id, task_label):
    log.info("开始处理数据,入参:account:%s,passwd:%s,products:%s", account, passwd, products)
    ip = get_host_ip()
    # 端口号默认从21503 开始，number 取第四位数字，但数量超过十个，端口号会进位，从59变成60 这里取两位计算
    number = int(str(port)[2:4]) - 50
    job_status = db.get_job_status(ip, port)
    if job_status['run_status'] == 1:
        log.info("ip:%s,port:%s的分片正在运行,请稍后请求", ip, port)
        return -1

    if job_status['run_status'] == 2:
        log.info("ip:%s,port:%s的分片正在启动app,请稍后请求", ip, port)
        return -1
    # 更新为运行状态
    db.update_job_status(ip, port, '1')
    try:
        status = get_memu_status(number)
        if status is False:
            restart_memu(number, ip, port)
        devices_addr = '127.0.0.1:' + str(port)
        time.sleep(5)
        p = multiprocessing.Process(target=run,
                                    args=(
                                        devices_addr, number, account, passwd, products, task_id, task_label, ip,
                                        port,))
        p.start()

        p.join()
        db.update_job_status(ip, port, '0')
    except Exception as e:
        log.info(traceback.format_exc())
        db.update_job_status(ip, port, '0')


def go_home(device):
    setup_page = device.xpath("地区设置").wait(timeout=2)
    if setup_page is not None:
        go_back(device, 1)
    device.xpath("首页").click_exists(timeout=5)


def heart(number, account, port):
    ip = get_host_ip()
    if get_memu_status(number) is False:
        log.info("程序未启动")
        return
    job_status = db.get_job_status_by_account(account)
    if job_status['run_status'] == 1:
        log.info("任务正在处理中,不进行心跳检测,%s", account)
        return
    try:
        log.info("心跳检测,number:%s", number)
        devices_addr = '127.0.0.1:' + port
        device = u2.connect(devices_addr)
        job_status = db.get_job_status_by_account(account)
        if job_status['run_status'] == 1:
            log.info("任务正在处理中,不进行心跳检测,%s", account)
            return
        device.xpath("我的淘宝").click_exists(timeout=5)
        time.sleep(1)
        job_status = db.get_job_status_by_account(account)
        if job_status['run_status'] == 1:
            log.info("任务正在处理中,不进行心跳检测,%s", account)
            return
        device.xpath("设置").click_exists(timeout=5)
        time.sleep(1)
        device.press("back")
        log.info("app运行正常")
    except Exception as e:
        log.info("心跳监控APP出现异常,重启", e)
        stop_memu(number)


def run(devices_addr, number, account, password, products, task_id, task_label, ip, port):
    log.info("开始润")
    try:
        global main_end
        main_end = False
        device=time_out_connect(devices_addr)
        time.sleep(2)
        random_policy = get_memu_policy(account)
        device.app_start("com.taobao.taobao")
        # 开启跳过广告线程
        threading.Thread(target=skip, args=(device,)).start()
        logged_account = get_memu_login_account(ip, port)
        log.info("当前模拟器登录的账号是:%s", logged_account)
        time.sleep(0.3)
        go_home(device)
        time.sleep(0.3)
        if account != logged_account:
            log.info("当前模拟器登录账号不一致,重新登录")
            db.insert_account_log(account, ip, port, '10', "账号更换登录")
            login(device, account, password)
        # 第一次打开app搜索会有个pre search 的提示，会吞掉操作，这里预先点击返回一次
        device.xpath('@com.taobao.taobao:id/searchbtn').wait()
        get_search_view(device).click_exists(timeout=10)
        go_back(device, 3)
        for item in products:
            device.xpath("我的淘宝").click_exists(timeout=5)
            time.sleep(1)
            device.xpath("设置").get(timeout=5)
            device.press("back")
            random_search(device, random_policy['search'], ip, port, account)
            if item.isdigit() is not True:
                log.info("商品id:%s不正确", str(item))
                continue
            url = 'http://detail.tmall.com/item.htm?id=' + str(item)
            click_search(device, url, random_policy, ip, port, account)
            time.sleep(1)
            valid_button = valid(device)
            if valid_button is not None:
                log.info("进程%s账号%s暂时失效", number, logged_account)
                db.update_account_info(account)
                db.insert_account_log(account, ip, port, '-1', "账号出现验证码")
                stop_memu(number)
                db.update_job_status(ip, port, '0')
                # 账号失效了就暂时不用了,这次请求直接结束
                break
            content = get_item_detail(devices=device, item_id=item, account=logged_account, index=number,
                                      conf=random_policy, ip=ip, port=port)
            db.update_info(content, item, task_id, task_label)
            db.insert_account_log(account, ip, port, '1', "账号获取商品详情")
            time.sleep(1)
            go_back(device, 3)
            start = random_policy['timeSleep']['begin']
            end = random_policy['timeSleep']['end']
            sleep_time = random.randint(int(start), int(end))
            log.info("账号%s休息%s秒", account, sleep_time)
            db.insert_account_log(account, ip, port, '2', "账号休息{}秒".format(sleep_time))
            time.sleep(sleep_time)

    except Exception as e:
        log.info(traceback.format_exc())
        # 出现异常终止操作 并终止app
        stop_memu(number)
    main_end = True
