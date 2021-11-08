import json
import os
import random
import traceback
from decimal import Decimal
import uiautomator2 as u2
import time
import subprocess
import multiprocessing
import threading
import MyLog
from timeit import default_timer
import db
import psutil
import socket
from func_timeout import func_set_timeout
import atexit
import requests
log = MyLog.Logger('CMT').get_log()


# 退出执行的方法
# @atexit.register
# def main_out_run():
#     log.info("main_out_run start")
#     account_infos = db.get_account_status(1)
#     for account in account_infos:
#         if account["run_status"] == 1:
#             try:
#                 psutil.Process(account['pid']).kill()
#             except:
#                 pass
#     log.info("main_out_run end")

@func_set_timeout(120)
def time_out_connect(addr):
    return u2.connect(addr)


# 检测滑块
def check_slider(devices, account, ip, port, watch=False, phone=True):
    pid = multiprocessing.current_process().pid
    tid = threading.current_thread().ident
    # 如果当前软件不是 taobao ,则终止滑块检测
    if devices.app_current() is None or devices.app_current().get('package') is None or devices.app_current().get(
            'package') != 'com.taobao.taobao':
        return True
    if devices.xpath('@android:id/decor_content_parent').exists is True:
        # 记录日志
        if watch is True:
            db.insert_account_log(account, ip, port, '-1', "pid=%s,tid=%s 异步检测-账号出现验证码" % (str(pid), str(tid)))
        else:
            db.insert_account_log(account, ip, port, '-1', "pid=%s,tid=%s 账号出现验证码" % (str(pid), str(tid)))
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
                                          pid=pid, tid=tid, startX=startX, startY=startY, endX=endX, endY=endY, s=s))
                devices.xpath("nc_1_refresh1").click()
                time.sleep(0.5)
                continue
            # 滑动成功
            if devices.xpath('@android:id/decor_content_parent').exists is False:
                db.insert_account_log(account, ip, port, '26',
                                      "pid={pid},tid={tid},拖动验证滑块成功 startX={startX},starY={startY},endX={endX},endY={endY},s={s}".format(
                                          pid=pid, tid=tid, startX=startX, startY=startY, endX=endX, endY=endY, s=s))
                return True
            time.sleep(1)
        # 滑块还在，设置为拖动失败
        if devices.xpath('@android:id/decor_content_parent').exists is True or devices.xpath(
                "nc_1_refresh1").exists is True:
            if phone is False:
                log.info("进程%s账号%s暂时失效", port, account)
                db.update_account_info(account)
                # stop_memu(port)
                return False
            else:
                # devices.app_stop("com.taobao.taobao")
                return False
        else:
            return True
    else:
        return True


def open_app(device):
    log.info("首屏监控启动")
    device.app_start("com.tunnelworkshop.postern")
    device.app_start("com.taobao.taobao")


def addWatch(device, account, ip, port):
    # device.watcher("check").when("@android:id/decor_content_parent").call(lambda d : check_slider(device, account, ip, port,True))
    device.watcher("taojinbiLoad").when("淘金币小镇正在拼命加载中").press("back")
    device.watcher("goldCoins").when("赚金币").press("back")
    device.watcher("home").when("信息").when("拨号").when("浏览器").when("相机").call(lambda d: open_app(device))
    device.watcher("net").when("网络竟然崩溃了").press("back")
    device.watcher.start(3)


# kill 进程执行的方法
def kill_exit_proc(account_infos):
    log.info("开始清除线程")
    for account in account_infos:
        if account["run_status"] == 1:
            try:
                psutil.Process(account['pid']).kill()
            except:
                pass
        db.update_account_status(account['port'],0)
    log.info("清除线程结束")
    return


# 息屏检测
def screen_on(device: u2.Device):
    # . 息屏检测
    if device.info["screenOn"] == False:
        device.press("power")
        device.swipe_ext("up", scale=0.9)


def app_start_check(device: u2.Device):
    # 1.息屏检测
    screen_on(device)
    running = device.app_list_running()
    if 'com.tunnelworkshop.postern' not in running:
        device.app_start('com.tunnelworkshop.postern')
    if 'com.taobao.taobao' not in running:
        device.app_start("com.taobao.taobao")
    # 当前软件是否是taobao
    if device.app_current().get('package') != 'com.taobao.taobao':
        device.app_start("com.taobao.taobao")
    # 退回到首页
    go_back_home(device)


def app_init(device: u2.Device):
    # 1.息屏检测
    screen_on(device)
    # 2.启动淘宝app
    device.app_start("com.tunnelworkshop.postern")
    time.sleep(0.3)
    device.app_start("com.taobao.taobao")


def go_back(devices, times):
    for i in range(times):
        devices.press("back")


def go_back_home(device):
     if device.xpath("首页").exists is True:
         device.xpath("首页").click()
     while device.xpath("首页").exists is False or device.xpath("扫一扫").exists is False or device.xpath("搜索").exists is False:
        go_back(device, 1)
        device.xpath("首页").wait(timeout=0.1)


# 获取搜索框坐标
def get_search_view(devices):
    return devices.xpath('@com.taobao.taobao:id/sv_search_view').child('/android.widget.FrameLayout')


# 获取搜索按钮坐标
def get_search_button(devices):
    return devices.xpath('@com.taobao.taobao:id/searchbtn')


def click_search(devices, name, random_policy, ip, port, account, phone):
    #如果当前搜索框存在 就不进行退回首页操作
    if devices.xpath("@com.taobao.taobao:id/edit_del_btn").exists is True:
        devices.xpath("@com.taobao.taobao:id/edit_del_btn").click()
        devices.xpath("@com.taobao.taobao:id/searchEdit").click()
    else:    # 随机策略完成后需要退回到首页
        go_back_home(devices)
        if phone is True:
            while True:
                if devices.xpath("扫一扫").exists is False:
                    go_back_home(devices)
                devices.xpath("扫一扫").parent().click()
                time.sleep(0.1)
                if devices.xpath("搜索").exists is False:
                    devices.press("back")
                else:
                    break
        else:
            get_search_view(devices).click_exists(timeout=10)
    devices.send_keys(name)
    if phone is True:
        devices.xpath("搜索").click()
    else:
        get_search_button(devices).click_exists(timeout=2)

@func_set_timeout(5)
def get_item_detail(item_id, devices, account, phone, sku):
    while devices.xpath("店内宝贝").exists is False and devices.xpath("加入购物车").exists is False and devices.xpath("@com.taobao.taobao:id/uik_public_menu_action_icon").exists is False and devices.xpath("试试其他相似宝贝").exists is False:
        time.sleep(0.1)
    exist = devices.xpath("商品过期不存在").exists
    exist2 = devices.xpath("宝贝不在了").exists
    exist3 = devices.xpath("很抱歉，您查看的宝贝不存在，可能已下架或被转移").exists
    if exist is True  or exist2 is True or exist3 is True:
        log.info("商品%s过期或不存在", item_id)
        return "商品%s过期或不存在"%(item_id)
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
    if sku is not None:
        devices.swipe_ext("up", scale=0.5)
        sku_info = get_item_sku_detail(devices)
        content += sku_info
    log.info("进程%s账号%s,获取商品%s数据:%s", str(multiprocessing.current_process().pid), account, item_id, content)
    return content


def get_item_sku_detail(devices):
    devices.xpath("选择").click()
    time.sleep(1)
    content = ''
    page_item = devices.xpath("@com.taobao.taobao:id/header").child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    time.sleep(0.3)
    if '券后' in content:
        return 'sku价格(' + page_item[4].text + ")"
    else:
        return 'sku价格(' + page_item[1].text + ")"


@func_set_timeout(300)
def run_item(device, ip, port, account, item, random_policy, task_id, task_label, phone, sku):
    db.update_job_status(ip, port, '1')
    if sku is not None:
        url = 'http://detail.tmall.com/item.htm?id=' + str(item) + '&skuId=' + str(sku)
    else:
        url = 'http://detail.tmall.com/item.htm?id=' + str(item)
    #搜索
    click_search(device, url, random_policy, ip, port, account, phone)
    time.sleep(0.1)
    # 判断是否出现验证码
    if check_slider(device, account, ip, port, False) is False:
        ##c 休眠5秒，抛出异常，
        time.sleep(2)
        raise RuntimeError('出现验证码，无法拖动')
    content = get_item_detail(devices=device, item_id=item, account=account, phone=phone, sku=sku)
    if content is not None:
        db.update_record_info(content, item, task_id, task_label, sku)
        db.update_account_info_date(account)
        db.insert_account_log(account, ip, port, '1', "账号获取商品详情")
    #
    go_back(device,1)
    #go_back_home(device)
    # start = random_policy['timeSleep']['begin']
    # end = random_policy['timeSleep']['end']
    # sleep_time = random.randint(int(start), int(end))
    # log.info("账号%s休息%s秒", account, sleep_time)
    # db.insert_account_log(account, ip, port, '2', "账号休息{}秒".format(sleep_time))
    # time.sleep(sleep_time)


def get_memu_policy(account):
    data = db.get_job_status_by_account(account)
    config = json.loads(data['config'])
    log.info("获得账号配置信息:%s", config)
    return config['random']


def run_items(device: u2.Device, account, products, task_id, task_label):
    # 获取账号动态配置信息
    random_policy = get_memu_policy(account['account'])
    # 再次进行检测
    app_start_check(device)
    for item in products:
        time_time = time.time()
        if '-' in item:
            #带有skuid，
            item_ids = str.split(item, '-')
            run_item(device, account['ip'], account['port'], account['account'], item_ids[0], random_policy, task_id,
                     task_label, True, item_ids[1])
        else:
            run_item(device, account['ip'], account['port'], account['account'], item, random_policy, task_id, task_label,
                     True, None)
        log.info((time.time()-time_time))
    return


def proc_run(account, array):
    # 记录线程，进程信息
    pid = multiprocessing.current_process().pid
    tid = threading.current_thread().ident
    db.insert_account_log(account['account'], account['ip'], account['port'], '30',
                          "pid=%s,tid=%s 进程启动" % (str(pid), str(tid)))
    db.update_job_pid(account['ip'], account['port'], pid)
    db.update_account_status(account['port'],1)
    device = None

    try:
        # 开始启动adb,taobao,postern
        device = time_out_connect(account['port'])
        addWatch(device,account['account'],account['ip'],account['port'])
    except:
        log.info("%s 连接失败"%(account['port']))
        db.update_account_status(account['port'], 0)
        raise Exception("%s 连接失败"%(account['port']))
    # app启动，初始化
    app_init(device)
    while True:
        data = get_task_data(account['port'])
        products = data['itemIds']
        task_id = data['taskId']
        task_label = data['taskLabel']
        if task_label is None or task_id is None or products is None:
            time.sleep(2)
            continue
        try:
            run_items(device=device, account=account, products=products, task_id=task_id, task_label=task_label)
        except:
            log.info(traceback.format_exc())
            app_init(device)
            app_start_check(device)
            pass
        app_start_check(device)

def get_task_data(port):
    get = requests.get("http://192.168.47.230:10003/product/getTaskData?port=%s"%(port))
    log.info("{port} 请求需要处理的数据 {result}".format(port=port,result=get.text))
    return json.loads(get.text)

# 注册退出方法
# atexit.register(main_out_run)
if __name__ == '__main__':
    array = multiprocessing.Manager().list()
    ALL_PROCESS = []
    # 1.查询有效的进程
    account_infos = db.get_account_status(1)
    # 2.kill 正在运行的进程
    kill_exit_proc(account_infos)
    # 3.启动进程
    for account in account_infos:
        db.insert_account_log(account['account'], account['ip'], account['port'], '29', "进程准备启动")
        current_process = multiprocessing.Process(target=proc_run, args=(account, array,), name=account['port'])
        current_process.start()
        ALL_PROCESS.append(current_process)
    time.sleep(5)
    while True:
        time.sleep(10)
        # 检测所有的账号有没有全部启动
        accounts = db.get_account_status(1)
        run_adb_code = []
        error_process = []
        for proc in ALL_PROCESS:
            if proc.is_alive():
                run_adb_code.append(proc.name)
                continue
            else:
                # 移除该线程
                #ALL_PROCESS.remove(proc)
                error_process.append(proc)
                log.info("进程=%s,porst=%s 结束，需要重启", proc.pid, proc.name)
                # 线程结束，需要重新启动
                # account = db.get_account_port(proc.name)
                # db.insert_account_log(account['account'], account['ip'], account['port'], '29', "进程准备启动")
                # current_process = multiprocessing.Process(target=proc_run, args=(account, array,), name=account['port'])
                # ALL_PROCESS.append(current_process)
                # current_process.start()
                # log.info("进程=%s,port=%s 启动成功，"%(current_process.pid, current_process.name))
        log.info("run process now,{pid},{run_adb_code}".format(pid=multiprocessing.current_process().pid,run_adb_code=run_adb_code))
        for proc in error_process:
            ALL_PROCESS.remove(proc)
        for account in accounts:
            if account['port'] not in run_adb_code:
                db.insert_account_log(account['account'], account['ip'], account['port'], '29', "进程准备启动")
                current_process = multiprocessing.Process(target=proc_run, args=(account, array,), name=account['port'])
                ALL_PROCESS.append(current_process)
                current_process.start()
                log.info("进程=%s,port=%s 启动成功"%(current_process.pid, current_process.name))
