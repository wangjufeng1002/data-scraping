import json
import multiprocessing
import random
import socket
import subprocess
import threading
import time
import traceback
from timeit import default_timer

import uiautomator2 as u2

import MyLog
import db

# 主线程运行标志,来让跳过弹窗的子线程能随主线程终止而结束
main_end = False
from func_timeout import func_set_timeout

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

def skip_special_page(devices):
    try:
        webWiew = devices.xpath("//android.webkit.WebView").all()
        for w in webWiew:
            if "金币小镇-首页" in w.text:
                devices.press("back")
    except:
        log.info("跳过金币小镇页面失败")


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


@func_set_timeout(120)
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
        if valid(devices,account, ip, port,False) is False:
            log.info("随机搜索出现验证")
            db.insert_account_log(account, ip, port, "-24", "账号随机搜索出现验证")
            time.sleep(1)
            go_back(devices, 4)
            return
        time.sleep(0.5)
        random_swipe(devices, False)
        time.sleep(1)
        go_back(devices, 3)


def click_search(devices, name, random_policy, ip, port, account, phone):
    # 随机策略
    # random_refresh(devices, random_policy['refresh'], ip, port, account)
    # random_shop_cart(devices, random_policy['shopCart'], ip, port, account)
    # random_message(devices, random_policy['message'], ip, port, account)
    # random_switch_tabs(devices, random_policy['switchTabs'], ip, port, account)
    #随机策略完成后需要退回到首页
    go_back_home(devices)
    if phone is True:
        ##devices.xpath(
         #   '//*[@resource-id="com.taobao.taobao:id/sv_search_view"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[5]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]').click()
        while True:
            time.sleep(0.3)
            if devices.xpath("扫一扫").exists is False:
                go_back_home(devices)
            devices.xpath("扫一扫").parent().click()
            time.sleep(0.3)
            if devices.xpath("搜索").exists is False:
                devices.press("back")
            else:
                break
    else:
        get_search_view(devices).click_exists(timeout=10)
    #time.sleep(0.5)

    devices.set_fastinput_ime(True)
    time.sleep(0.3)
    devices.send_keys(name)
    time.sleep(0.5)
    if phone is True:
        devices.xpath("搜索").click()
    else:
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
        devices.swipe_ext("up", scale=0.5)
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
        tabs = devices.xpath("@com.taobao.taobao:id/rv_main_container").child("//android.widget.HorizontalScrollView").child("//android.widget.TextView").all()
        if len(tabs) <= 0:
            return
        index = random.randint(0, len(tabs) - 1)
        tabs[index].click()
        time.sleep(1)


def get_item_detail(item_id, devices, account, index, conf, ip, port, phone, sku):
    exist = devices.xpath("商品过期不存在").wait(timeout=1)
    exist2 =devices.xpath("宝贝不在了").wait(timeout=1)
    exist3 = devices.xpath("很抱歉，您查看的宝贝不存在，可能已下架或被转移").wait(timeout=1)
    if exist is not None or exist2 is not None or exist3 is not None:
        log.info("商品%s过期或不存在", item_id)
        return "商品%s过期或不存在".format(item_id)
    devices.xpath('@com.taobao.taobao:id/uik_public_menu_action_icon').wait()
    content = ''
    devices.swipe_ext("up", scale=0.5)
    resource_id = '@com.taobao.taobao:id/mainpage'
    if phone is True:
        resource_id = '@com.taobao.taobao:id/mainpage2'
    page_item = devices.xpath(resource_id).child('//android.widget.TextView').all()
    # 有些商品页面用的组件id又不一样，这里两个id都查
    if len(page_item) == 0:
        page_item = devices.xpath("@com.taobao.taobao:id/mainpage").child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    time.sleep(0.3)
    if sku is not None:
        devices.swipe_ext("up", scale=0.5)
        sku_info = get_item_sku_detail(devices)
        content += sku_info
    log.info("进程%s账号%s,获取商品%s数据:%s", str(index), account, item_id, content)
    # random_comment(devices, conf['comment'], ip, port, account)

    # time.sleep(1)
    return content


def get_item_sku_detail(devices):
    devices.xpath("选择").click()
    time.sleep(1)
    content = ''
    page_item = devices.xpath("@com.taobao.taobao:id/header").child('//android.widget.TextView').all()
    for item in page_item:
        if item.text !=  '':
            content += item.text
    time.sleep(0.3)
    if '券后' in content:
        return 'sku价格(' + page_item[4].text+")"
    else:
        return 'sku价格(' + page_item[1].text + ")"


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
#校验处理滑块
def check_slider(devices,account, ip, port,watch=False,phone=True):
    pid = multiprocessing.current_process().pid
    tid = threading.current_thread().ident
    #如果当前软件不是 taobao ,则终止滑块检测
    if devices.app_current() is None or devices.app_current().get('package') is None or devices.app_current().get('package') != 'com.taobao.taobao':
        return True
    if  devices.xpath('@android:id/decor_content_parent').exists is True:
        # 记录日志
        if watch is True:
            db.insert_account_log(account, ip, port, '-1',"pid=%s,tid=%s 异步检测-账号出现验证码"%(str(pid),str(tid)))
        else:
            db.insert_account_log(account, ip, port, '-1',"pid=%s,tid=%s 账号出现验证码"%(str(pid),str(tid)))
        log.info("手机上出现验证")
        for i in range(1, 3):
            # 是否需要刷新
            if devices.xpath("nc_1_refresh1").exists is True:
                devices.xpath("nc_1_refresh1").click()
                time.sleep(0.5)
            startX = 165  # 开始 x 坐标
            startY = 1356  # 开始 y 轴坐标
            endX = random.randint(945, 1000)  # 结束坐标
            endY = 1470  # 结束Y轴坐标
            s = random.randint(1, 9) / 100
            # 拖动滑块
            if devices.xpath('@android:id/decor_content_parent').exists is True:
                devices.swipe_points([(startX, startY), (endX, endY)], s)
            time.sleep(0.5)
            # 滑动失败
            if devices.xpath("nc_1_refresh1").exists is True:
                db.insert_account_log(account, ip, port, '27',
                                      "pid={pid},tid={tid},拖动验证滑块失败 startX={startX},starY={startY},endX={endX},endY={endY},s={s}".format(
                                          pid=pid, tid=tid,startX=startX, startY=startY, endX=endX, endY=endY, s=s))
                devices.xpath("nc_1_refresh1").click()
                time.sleep(0.5)
                continue
            # 滑动成功
            if devices.xpath('@android:id/decor_content_parent').exists is False:
                db.insert_account_log(account, ip, port, '26',
                                      "pid={pid},tid={tid},拖动验证滑块成功 startX={startX},starY={startY},endX={endX},endY={endY},s={s}".format(
                                          pid=pid,tid=tid,startX=startX, startY=startY, endX=endX, endY=endY, s=s))
                return True
            time.sleep(1)
        #滑块还在，设置为拖动失败
        if devices.xpath('@android:id/decor_content_parent').exists is True or devices.xpath("nc_1_refresh1").exists is True:
            if phone is False:
                log.info("进程%s账号%s暂时失效", port,account)
                db.update_account_info(account)
                stop_memu(port)
                return False
            else:
                #devices.app_stop("com.taobao.taobao")
                return False
        else:
            return True
    else:
        return True



def valid(devices,account, ip, port,watch=False):
    #如果存在验证
    if devices.xpath('@android:id/decor_content_parent').exists is True:
        #记录日志
        if watch is True:
            db.insert_account_log(account, ip, port, '-1', "异步检测-账号出现验证码")
        else:
            db.insert_account_log(account, ip, port, '-1', "账号出现验证码")
        log.info("手机上出现验证")
        time.sleep(0.5)
        for i in range(1,5):
            #是否需要刷新
            if devices.xpath("nc_1_refresh1").exists is True:
                devices.xpath("nc_1_refresh1").click()
                time.sleep(0.5)
            startX = 165 #开始 x 坐标
            startY=1356  #开始 y 轴坐标
            endX = random.randint(945,1000) #结束坐标
            endY = 1470                     #结束Y轴坐标
            s= random.randint(1,9)/100
            #拖动滑块
            devices.swipe_points([(startX, startY), (endX, endY)], s)
            time.sleep(0.5)
            #滑动失败
            if devices.xpath("nc_1_refresh1").exists is True:
                db.insert_account_log(account, ip, port, '27', "拖动验证滑块失败 startX={startX},starY={startY},endX={endX},endY={endY},s={s}".format(startX=startX,startY=startY,endX=endX,endY=endY,s=s))
                devices.xpath("nc_1_refresh1").click()
                time.sleep(0.5)
            #滑动成功
            if devices.xpath('@android:id/decor_content_parent').exists is False:
                db.insert_account_log(account, ip, port, '26',  "拖动验证滑块成功 startX={startX},starY={startY},endX={endX},endY={endY},s={s}".format(startX=startX,startY=startY,endX=endX,endY=endY,s=s))
                return True
            time.sleep(1)
        return False
    else:
        return True


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
                                        devices_addr, number, account, products, task_id, task_label, ip,
                                        port, False))
        p.start()

        p.join()
        db.update_job_status(ip, port, '0')
    except Exception as e:
        log.info(traceback.format_exc())
    finally:
        db.update_job_status(ip, port, '0')


def go_back_home(device):
    page = device.xpath("首页").wait(timeout=0.1)
    while page is None:
        go_back(device, 1)
        page = device.xpath("首页").wait(timeout=0.1)


def go_home(device):
    setup_page = device.xpath("地区设置").wait(timeout=2)
    if setup_page is not None:
        go_back(device, 1)
    device.xpath("首页").click_exists(timeout=5)

def heart( account, addr):
    job_status = db.get_job_status_by_account(account)
    device = u2.connect(addr)
    #1. 息屏检测
    if device.info["screenOn"] == False:
        device.press("power")
        device.swipe_ext("up", scale=0.9)
    #2.连续充电时间长
    if device.xpath("好").exists is True:
        device.xpath("好").click()
    # #3.检测验证码
    # valid_button = valid(device, job_status['account'], job_status['ip'], job_status['port'],False)
    # if valid_button is False:
    #     #db.insert_account_log(account, job_status['ip'], job_status['port'], '-1', "账号出现验证码")
    #     #log.info("手机上出现验证")
    #     #time.sleep(1)
    #     # 出现验证重启app
    #     device.app_stop("com.taobao.taobao")
    #     time.sleep(1)
    #     # device.app_start("com.taobao.taobao")
    #     db.update_job_status(job_status['ip'], job_status['port'], 0)
    #     return
    #4.检测任务运行态
    if job_status['run_status'] == 1:
        log.info("任务正在处理中,不进行心跳检测,%s", account)
        return
    try:

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
        log.info("account:%s,addr:%s app运行正常",account,addr)
    except Exception as e:
        log.info("心跳监控APP出现异常,重启", e)
        restart_app_func(device)
        # stop_memu(number)


@func_set_timeout(300)
def run_item(device, ip, port, account, item, random_policy, number, logged_account, task_id, task_label, phone, sku):
    db.update_job_status(ip, port, '1')
    #跳过特殊页面
    skip_special_page(device)
    if phone is False:
        random_search(device, random_policy['search'], ip, port, account)
    if item.isdigit() is not True:
        log.info("商品id:%s不正确", str(item))
        return
    if sku is not None:
        url = 'http://detail.tmall.com/item.htm?id=' + str(item) + '&skuId=' + str(sku)
    else:
        url = 'http://detail.tmall.com/item.htm?id=' + str(item)
    click_search(device, url, random_policy, ip, port, account, phone)
    time.sleep(0.5)
    #判断是否出现验证码
    if check_slider(device,account,ip,port,False) is False:
        ##c 休眠5秒，抛出异常，
        time.sleep(5)
        raise RuntimeError('出现验证码，无法拖动')
    #判断是否出现验证码
    # valid_button = valid(device,account, ip, port,False)
    # if valid_button is False:
    #     if phone is False:
    #         log.info("进程%s账号%s暂时失效", number, logged_account)
    #         db.update_account_info(account)
    #         db.insert_account_log(account, ip, port, '-1', "账号出现验证码")
    #         stop_memu(number)
    #         db.update_job_status(ip, port, '0')
    #         # 账号失效了就暂时不用了,这次请求直接结束
    #         return
    #     else:
    #         #db.insert_account_log(account, ip, port, '-1', "账号出现验证码")
    #         #log.info("手机上出现验证")
    #         time.sleep(1)
    #         #出现验证重启app
    #         device.app_stop("com.taobao.taobao")
    #         #device.app_start("com.taobao.taobao")
    #         db.update_job_status(ip,port,0)
    #         return

    content = get_item_detail(devices=device, item_id=item, account=logged_account, index=number,
                              conf=random_policy, ip=ip, port=port, phone=phone, sku=sku)
    if content is not None and len(content) > 0:
        db.update_info(content, item, task_id, task_label,sku)
        db.update_account_info_date(account)
        db.insert_account_log(account, ip, port, '1', "账号获取商品详情")
    time.sleep(0.3)
    go_back_home(device)
    # start = random_policy['timeSleep']['begin']
    # end = random_policy['timeSleep']['end']
    # sleep_time = random.randint(int(start), int(end))
    # log.info("账号%s休息%s秒", account, sleep_time)
    # db.insert_account_log(account, ip, port, '2', "账号休息{}秒".format(sleep_time))
    # time.sleep(sleep_time)


def run_phone(devices_addr, number, account, products, task_id, task_label, port):
    log.info("本次手机%s抓取商品%s", devices_addr, products)
    ip = get_host_ip()
    job_status = db.get_job_status(ip, port)
    if job_status['run_status'] == 1:
        log.info("ip:%s,port:%s的分片正在运行,请稍后请求", ip, port)
        return -1
    try:
        #创建进程标识文件
        if db.update_job_status_lock(ip, port, 1) < 1:
            return
        db.insert_account_log(account, ip, port, '29', "进程准备启动")
        p = multiprocessing.Process(target=run,
                                    args=(
                                        devices_addr, number, account, products, task_id, task_label, ip,
                                        port, True))
        p.start()
        p.join()
        db.update_job_status(ip, port, 0)
    except Exception as e:
        log.info(traceback.format_exc())
        db.update_job_status(ip, port, 0)


def run(devices_addr, number, account, products, task_id, task_label, ip, port, phone=False):
    device = None
    try:
        pid = multiprocessing.current_process().pid
        tid = threading.current_thread().ident
        db.insert_account_log(account, ip, port, '30', "pid=%s,tid=%s 进程启动" % (str(pid), str(tid)))
        #写入进程编号
        db.update_job_pid(ip,port,pid)
        global main_end
        main_end = False
        device = time_out_connect(devices_addr)
        #. 息屏检测
        if device.info["screenOn"] == False:
           device.press("power")
           device.swipe_ext("up", scale=0.9)
        #time.sleep(2)
        random_policy = get_memu_policy(account)
        #添加滑块监控
        addWatch(device,account,ip,port)
        # 启动代理app todo 自动配置代理ip
        device.app_start("com.tunnelworkshop.postern")
        device.app_stop("com.taobao.taobao")
        go_back(device, 1)
        time.sleep(1)
        device.app_start("com.taobao.taobao")
        db.insert_account_log(account, ip, port, '3', "pid=%s,tid=%s APP 淘宝启动" % (str(pid), str(tid)))
        # 开启跳过广告线程
        # threading.Thread(target=skip, args=(device,)).start()
        logged_account = get_memu_login_account(ip, port)
        log.info("当前模拟器登录的账号是:%s", logged_account)
        time.sleep(0.3)
        go_home(device)
        time.sleep(0.3)
        if phone is False:
            # 第一次打开app搜索会有个pre search 的提示，会吞掉操作，这里预先点击返回一次
            device.xpath('@com.taobao.taobao:id/searchbtn').wait()
            get_search_view(device).click_exists(timeout=10)
            time.sleep(3)
            go_back(device, 3)
            # 这里由于性能问题，启动卡顿等原因，可能莫名其妙吞操作,导致app退出,这里检测一下 如果app被退出，就重新启动
            running = device.app_list_running()
            if 'com.taobao.taobao' not in running:
                device.app_start("com.taobao.taobao")
        for item in products:
            # 异常退出自重启
            running = device.app_list_running()
            if 'com.taobao.taobao' not in running:
                device.app_start("com.taobao.taobao")
            if '-' in item:
                # 带有skuid，
                item_ids = str.split(item, '-')
                run_item(device, ip, port, account, item_ids[0], random_policy, number, logged_account, task_id,
                         task_label, phone, item_ids[1])
            else:
                run_item(device, ip, port, account, item, random_policy, number, logged_account, task_id, task_label,
                         phone, None)
    except Exception as e:
        log.info(traceback.format_exc())
        db.update_job_status(ip, port, '0')
        # 出现异常终止操作 并终止app
        if phone is False:
            stop_memu(number)
    finally:
        if device is not  None:
            device.watcher.stop()
    main_end = True
    db.update_job_status(ip, port, '0')

def open_app(device):
    log.info("首屏监控启动")
    device.app_start("com.tunnelworkshop.postern")
    device.app_start("com.taobao.taobao")

def addWatch(device,account,ip,port):
    #device.watcher("check").when("@android:id/decor_content_parent").call(lambda d : check_slider(device, account, ip, port,True))
    device.watcher("taojinbiLoad").when("淘金币小镇正在拼命加载中").press("back")
    device.watcher("goldCoins").when("赚金币").press("back")
    device.watcher("home").when("信息").when("拨号").when("浏览器").when("相机").call(lambda d:open_app(device))
    device.watcher.start(3)


if __name__ == '__main__':
    begin =26.0
    for  i in range(0,400):
        end =begin+0.1
        url ='"https://bokuts.tmall.com/search.htm?tsearch=y&search=y&orderType=newOn_desc&viewType=grid&keyword=&lowPrice={}&highPrice={}",'
        a=format(begin,'.1f')
        b=format(end,'.1f')
        print(url.format(a,b))
        begin+=0.1