import json
import multiprocessing
import os
import random
import re
import threading
import time
import traceback

import psutil
import requests
import uiautomator2 as u2
from func_timeout import func_set_timeout

import MyLog
import db

log = None
img_path = 'D:\\logs\\cmt\\img\\'


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
                return False
            else:
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
        db.update_account_status(account['port'], 0)
    log.info("清除线程结束")
    return


# 息屏检测
def screen_on(device: u2.Device):
    # . 息屏检测
    if device.info["screenOn"] == False:
        device.press("power")
        device.swipe_ext("up", scale=0.9)


def app_start_check(device: u2.Device):
    log.info("app_start_check start")
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
    log.info("app_start_check end")


def app_init(device: u2.Device):
    log.info("app_init start")
    # 1.息屏检测
    screen_on(device)
    # 2.启动淘宝app
    device.app_start("com.tunnelworkshop.postern")
    time.sleep(0.3)
    device.app_start("com.taobao.taobao")
    log.info("app_init end")

def app_restart(device: u2.Device):
    log.info("app_restart start")
    device.app_start(package_name="com.taobao.taobao",stop=True)
    log.info("app_restart end")


def go_back(devices, times):
    log.info(" go_back start ")
    for i in range(times):
        devices.press("back")
    log.info(" go_back end ")

@func_set_timeout(60)
def go_back_home(device):
    log.info(" go_back_home start")
    while device.xpath("推荐").exists is False or device.xpath("扫一扫").exists is False or device.xpath(
            "搜索").exists is False:
        if device.xpath("首页").exists is True:
            device.xpath("首页").click()
        else:
            go_back(device, 1)
            device.xpath("首页").wait(timeout=0.1)
    log.info(" go_back_home end")


# 获取搜索框坐标
def get_search_view(devices):
    return devices.xpath('@com.taobao.taobao:id/sv_search_view').child('/android.widget.FrameLayout')


# 获取搜索按钮坐标
def get_search_button(devices):
    return devices.xpath('@com.taobao.taobao:id/searchbtn')

def close_useless_popup(device):
    # 看下有没有弹窗
    if device.xpath("受疫情影响，当前地区商品送达可能会有延迟").exists:
        parent = device.xpath("受疫情影响，当前地区商品送达可能会有延迟").parent().parent()
        child = device.xpath(parent.get_xpath()).child("//android.widget.ImageView").all()
        child[len(child)-1].click()
        # for c in child:
        #     c.click()
def go_back_list(device,query_key):
    while True:
        if device.xpath(query_key).exists is False:
            device.press("back")
        else:
            break
#@func_set_timeout(10)
def click_search(devices, name,port, phone):
    # 如果当前搜索框存在 就不进行退回首页操作
    edit_del = devices.xpath("@com.taobao.taobao:id/edit_del_btn").wait(0.1)
    if edit_del is not None and devices.xpath("@com.taobao.taobao:id/edit_del_btn").exists is True:
        devices.xpath("@com.taobao.taobao:id/edit_del_btn").click()
        devices.xpath("@com.taobao.taobao:id/searchEdit").click()
    else:  # 随机策略完成后需要退回到首页
        log.info(" run_item.click_search go back home start,port={}".format(port))
        go_back_home(devices)
        if phone is True:
            while True:
                if devices.xpath("扫一扫").exists is False or devices.xpath("搜索").exists is False:
                    go_back_home(devices)
                else:
                    devices.xpath("扫一扫").parent().click()
                    time.sleep(0.1)
                    break
        else:
            get_search_view(devices).click_exists(timeout=10)
        log.info(" run_item.click_search go back home start,port={}".format(port))
    devices.set_fastinput_ime(True)
    devices.send_keys(name)
    if devices.xpath(name).wait(0.1) is None or devices.xpath(name).exists is False:
        raise Exception("输入失败，需要重新定位")
    if phone is True:
        devices.xpath("搜索").click()
    else:
        get_search_button(devices).click_exists(timeout=2)


#@func_set_timeout(30)
def get_item_detail(item_id, devices, account, phone, sku):
    while devices.xpath("加入购物车").exists is False and devices.xpath("店内宝贝").exists is False and devices.xpath(
            "@com.taobao.taobao:id/uik_public_menu_action_icon").exists is False and devices.xpath(
        "试试其他相似宝贝").exists is False:
        pass
    exist = devices.xpath("商品过期不存在").exists
    exist2 = devices.xpath("宝贝不在了").exists
    exist3 = devices.xpath("很抱歉，您查看的宝贝不存在，可能已下架或被转移").exists
    exist4 = devices.xpath("商品已经下架啦~要不要瞧瞧别的~").exists
    if exist is True or exist2 is True or exist3 is True or exist4 is True:
        log.info("商品%s过期或不存在", item_id)
        return "商品%s过期或不存在" % (item_id)
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
        devices.swipe_ext("up", scale=0.7)
        sku_info = get_item_sku_detail(devices)
        content += sku_info
    log.info("进程%s账号%s,获取商品%s数据:%s", str(multiprocessing.current_process().pid), account, item_id, content)
    return content
#获取已选中的sku名称
def get_select_sku_name(device, frame):
    layout__all = device.xpath(frame.get_xpath()).child("//android.widget.LinearLayout").all()
    # 如果是空，则再往上找一级，获取lay_out标签
    if layout__all is None or len(layout__all) == 0:
        parent = device.xpath(frame.get_xpath()).parent()
        layout__all = device.xpath(parent.get_xpath()).child("//android.widget.LinearLayout").all()
    for lay_out in layout__all:
        desc_ = lay_out.attrib['content-desc']
        if '已选中' in desc_:
            return desc_
    return None


def get_sku_name_2(device):
    edition_text=None
    fascicle_text=None
    subject_text=None
    apply_text=None
    sku_valid=False
    while True:
        frame_layouts= device.xpath("@com.taobao.taobao:id/body").child("/android.widget.FrameLayout").all()
        for frame in frame_layouts:
            text_view = device.xpath(frame.get_xpath()).child("//android.widget.TextView")
            if text_view.exists is False:
                continue

            if any(val in text_view.get_text() for val in ['科目','更多版本','分册名','适用地区']):
                text = get_select_sku_name(device, frame)
            else:
                continue
            if text is not None:
                sku_valid = True
            if subject_text is None and subject_text !='' and '科目' in text_view.get_text():
                subject_text = text
            if edition_text is None and edition_text != '' and  '更多版本' in text_view.get_text():
                edition_text = text
            if fascicle_text is None and fascicle_text != '' and '分册名' in text_view.get_text():
                fascicle_text = text
            if apply_text is None and apply_text != '' and '适用地区' in text_view.get_text():
                apply_text = text
                ##查看是否有已选中的标签
        if device.xpath("购买数量").exists is False:
            device.swipe_ext("up", scale=0.7)
        else:
            break
    if edition_text is not None:
        edition_text = edition_text.replace("已选中 ","").replace("已选中","")
        edition_text = "版本:"+edition_text+";"
    else:
        edition_text = ''
    if fascicle_text is not None:
        fascicle_text = fascicle_text.replace("已选中 ", "").replace("已选中", "")
        fascicle_text = "分册名: "+fascicle_text+";"
    else:
        fascicle_text = ''
    if subject_text is not None:
        subject_text = subject_text.replace("已选中 ", "").replace("已选中", "")
        subject_text = "科目: " + subject_text + ";"
    else:
        subject_text = ''
    if apply_text is not None:
        apply_text = apply_text.replace("已选中 ", "").replace("已选中", "")
        apply_text = "适用地区: " + apply_text + ";"
    else:
        apply_text = ''
    skuName = 'sku名称(' + edition_text + fascicle_text + subject_text + apply_text +")"
    if sku_valid is False:
        skuName = skuName + "sku已失效"
    return skuName

def get_item_sku_detail(devices):
    if devices.xpath("选择").exists is False:
        return ""
    devices.xpath("选择").click()
    time.sleep(1)
    content = ''
    page_item = devices.xpath("@com.taobao.taobao:id/header").child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    time.sleep(0.3)
    price_result_str = ''
    price_default_str=''
    #sku券后价
    if '券后' in content:
        try:
            val = re.search("(券后|折后)￥(.+?)[\d.]+", content, re.S).group(0).replace("券后￥", "").replace("折后￥", "")
            price_result_str = val
        except:
            price_result_str = page_item[4].text
    #sku页面价
    try:
        val = re.search("￥(.+?)[\d.]+", content, re.S).group(0).replace("￥", "")
        price_default_str = val
    except:
        try:
            price_default_str = page_item[1].text
        except:
            pass
    price_return = ''
    if price_result_str is None or price_result_str == '':
        price_result_str = price_default_str

    # 特殊处理
    if price_default_str is None or price_default_str == '':
        price_return += "sku页面价格(" + " " + ")"
    else:
        price_return += "sku页面价格(" + str(price_default_str) + ")"

    if price_result_str is None or price_result_str == '':
        price_return += "sku到手价格(" + " " + ")"
    else:
        price_return += "sku到手价格(" + str(price_result_str) + ")"

    skuInfo = get_sku_name_2(devices)
    return  (price_return + skuInfo)
#最低价-详细信息获取
def get_lowest_detail(device,phone,port):
    # 关闭下无用弹窗
    close_useless_popup(device)
    while device.xpath("加入购物车").exists is False and device.xpath("店内宝贝").exists is False and device.xpath(
            "@com.taobao.taobao:id/uik_public_menu_action_icon").exists is False and device.xpath(
        "试试其他相似宝贝").exists is False:
        pass
    exist = device.xpath("商品过期不存在").exists
    exist2 = device.xpath("宝贝不在了").exists
    exist3 = device.xpath("很抱歉，您查看的宝贝不存在，可能已下架或被转移").exists
    exist4 = device.xpath("商品已经下架啦~要不要瞧瞧别的~").exists
    if exist is True or exist2 is True or exist3 is True or exist4 is True:
        #log.info("商品%s过期或不存在", item_id)
        return "商品过期或不存在"
    device.xpath('@com.taobao.taobao:id/uik_public_menu_action_icon').wait()
    content = ''
    #上划0.5
    device.swipe_ext("up", scale=0.5)
    resource_id = '@com.taobao.taobao:id/mainpage'
    if phone is True:
        resource_id = '@com.taobao.taobao:id/mainpage2'
    page_item = device.xpath(resource_id).child('//android.widget.TextView').all()
    # 有些商品页面用的组件id又不一样，这里两个id都查
    if len(page_item) == 0:
        page_item = device.xpath("@com.taobao.taobao:id/mainpage").child('//android.widget.TextView').all()
    for item in page_item:
        if item.text != '':
            content += item.text
    #开始下滑获取 基本信息，和 店铺名称
    base_dic = {}
    while True:
        # 关闭下无用弹窗
        close_useless_popup(device)
        if device.xpath("参数").exists is True or device.xpath("产品参数").exists is True:
            if device.xpath("参数").exists is True:
                 device.xpath("参数").click()
            if device.xpath("产品参数").exists is False:
                continue
            if device.xpath("@com.taobao.taobao:id/lv_data").exists :
                #这里应该有个小循环
                loop = 0
                while loop < 2:
                    container_all = device.xpath("@com.taobao.taobao:id/container").all()
                    for container in container_all:
                        child_el = device.xpath(container.get_xpath()).child('//android.widget.TextView').all()
                        if len(child_el) >=2:
                            base_dic[child_el[0].text]=child_el[1].text
                    device.swipe_ext("up", scale=0.3)
                    loop+=1
                print(base_dic)
                device.xpath("完成").click()
                break
        else:
            device.swipe_ext("up", scale=0.5)
    #店铺名称
    shop_name=''
    shop_name_loop_total = 5
    shop_name_loop_index = 0
    while shop_name_loop_index < shop_name_loop_total:
        # 关闭下无用弹窗
        close_useless_popup(device)
        if device.xpath("进店逛逛").exists is True:
            parent = device.xpath("进店逛逛").parent()
            while True:
                if parent.attrib['content-desc'] != None and parent.attrib['content-desc'] != '':
                    parent = device.xpath(parent.get_xpath()).parent()
                else:
                    break
            view__all = device.xpath(parent.get_xpath()).child("//android.widget.TextView").all()
            shop_name = view__all[0].text
            print(shop_name)
            break
        else:
            shop_name_loop_index += 1
            device.swipe_ext("up", scale=0.5)
    #短连接
    if device.xpath("ꄪ").exists is False:
        device.xpath("@com.taobao.taobao:id/uik_public_menu_action_icon").click()
    else:
        device.xpath("ꄪ").click()
    time.sleep(0.3)
    device.xpath("复制链接").click()
    copy_text = device.clipboard
    short_url = re.search(u"】(.+?)「", copy_text).group(0).replace("】", '').replace('「', '').replace(' ', '')
    device.set_clipboard('text', '')
    try:
        device.xpath("取消").click()
    except:
        pass

    ##拼接结果
    #拼接短连接
    content += '<@ ' + port + ' @>'
    content+="<shortUrl>"+short_url+"</shortUrl>"
    content+="<shopName>"+shop_name +"</shopName>"
    content+="<basicInfo>"+ json.dumps(base_dic, ensure_ascii=False) +"</basicInfo>"
    ##单独返回下 Url, shop_name,基础信息等
    result ={}
    result['shop_name']=shop_name
    result['short_url'] = short_url
    result['basic_info'] = json.dumps(base_dic, ensure_ascii=False)
    result['original_info'] = content
    #回到列表页
    device.press("back")
    return  result



#最低价-列表处理
def get_lowest_item_list(device,port,query_key,proc_dict):
    # device.send_keys("9787505733183")
    #判断下 价格是否单独是一个选择
    if device.xpath("价格").exists is True:
        # 点击排序选择
        device.xpath("@com.taobao.taobao:id/up_arrow").click()
    else:
        device.xpath("@com.taobao.taobao:id/arrow").click()
        # 选择价格升序
        if device.xpath("价格升序").exists is True:
            device.xpath("价格升序").long_click()
        elif device.xpath("价格").exists is True:
            # 点击排序选择
            device.xpath("@com.taobao.taobao:id/up_arrow").click()
        else:
            return

    #休眠一下
    time.sleep(1)
    suc_name = set()
    suc_result = []
    while True:
        proc_dict[multiprocessing.current_process().pid] = int(time.time())
        # 选择列表
        recycler__all = device.xpath('@com.taobao.taobao:id/libsf_srp_header_list_recycler').child(
            '/android.widget.FrameLayout').all()
        # 遍历所有品信息
        for item in recycler__all:
            proc_dict[multiprocessing.current_process().pid] = int(time.time())
            views = device.xpath(item.get_xpath()).child("//android.view.View").all()
            # 遍历一下品信息，看看是否时二手书
            for view in views:
                proc_dict[multiprocessing.current_process().pid] = int(time.time())
                if '根据大部分用户的喜爱为您挑选以下商品' in view.attrib['content-desc']:
                    break
                desc = view.attrib['content-desc']
                if desc is None or desc == '':
                    continue
                if '二手' in desc or '闲鱼' in desc or '电子书' in desc or '电子版' in desc or '印刷' in desc or '有声内容' in desc or '商品不存在等' in desc:
                    print('不合法的商品 = ' + view.attrib['content-desc'])
                    break
                if '进店' in desc or '更多' in desc:
                    continue
                print('合法 = ' + view.attrib['content-desc'])
                if view.attrib['content-desc'] in suc_name:
                    continue
                suc_name.add(view.attrib['content-desc'])
                #跳转到详情进行处理
                device.xpath(view.get_xpath()).click()
                time.sleep(0.5)
                #关闭下无用弹窗
                close_useless_popup(device)
                proc_dict[multiprocessing.current_process().pid] = int(time.time())
                detail = get_lowest_detail(device, True, port=port)
                proc_dict[multiprocessing.current_process().pid] = int(time.time())
                suc_result.append(detail)
                #回到列表页
                go_back_list(device, query_key=query_key)
            #这里再判断下是否回到了列表页
            go_back_list(device,query_key=query_key)
        if len(suc_name) >=10:
            break
        device.swipe_ext("up", scale=1.0)
        if device.xpath("没有更多内容了").exists:
            break
    return suc_result



@func_set_timeout(300)
def run_item(device, ip, port, account, item, random_policy, task_id, task_label, phone, sku):
    global log
    if log is None:
        log = MyLog.Logger(port).get_log()
    if sku is not None:
        url = 'http://detail.tmall.com/item.htm?id=' + str(item) + '&skuId=' + str(sku)
    else:
        url = 'http://detail.tmall.com/item.htm?id=' + str(item)
    # 搜索
    log.info(" run_item.click_search start,port={}".format(port))
    click_search(device, url, port, phone)
    log.info(" run_item.click_search end,port={}".format(port))
    db.update_job_status(ip, port, '1')
    # 判断是否出现验证码
    if check_slider(device, account, ip, port, False) is False:
        ##c 休眠5秒，抛出异常，
        time.sleep(2)
        raise RuntimeError('出现验证码，无法拖动')
    time_time = time.time()
    try:
        content = get_item_detail(devices=device, item_id=item, account=account, phone=phone, sku=sku)
        if content is not None:
            content += '<@ '+port+' @>'
            db.update_record_info(content, item, task_id, task_label, sku)
            db.update_account_info_date(account)
            db.insert_account_log(account, ip, port, '1', "账号获取商品详情")
    except:
        log.error("run_item exception,port={}".format(port))
        log.error(traceback.format_exc())
        pass
    else:
        go_back(device, 1)
    log.info("账号%s-%s 抓取 %s 详情所用时间 %d" % (account, port, item, (time.time() - time_time)))
    #

    # go_back_home(device)
    # start = random_policy['timeSleep']['begin']
    # end = random_policy['timeSleep']['end']
    # sleep_time = random.randint(int(start), int(end))
    # log.info("账号%s休息%s秒", account, sleep_time)
    # db.insert_account_log(account, ip, port, '2', "账号休息{}秒".format(sleep_time))
    # time.sleep(sleep_time)

def run_item_lowest(device, ip, port, account, task_id, task_label, phone,product_isbn,proc_dict):
    global log
    if log is None:
        log = MyLog.Logger(port).get_log()
    # 搜索
    log.info("run_item_lowest.click_search start,port={}".format(port))
    if len(product_isbn.split("-")) < 2:
        return
    dd_product_id = product_isbn.split("-")[0]
    ##isBN为空
    isbn = product_isbn.split("-")[1]
    if isbn is None or len(isbn) == 0:
        return
    #搜索
    click_search(device, isbn, port,phone)
    time.sleep(0.5)
    log.info(" run_item_lowest.click_search end,port={}".format(port))
    db.update_job_status(ip, port, '1')
    # 判断是否出现验证码
    if check_slider(device, account, ip, port, False) is False:
        #休眠5秒，抛出异常，
        time.sleep(2)
        raise RuntimeError('出现验证码，无法拖动')
    #判断下有没有找到商品
    if device.xpath("没有找到相关产品").exists:
        db.update_lowest_price_result(task_id=task_id,task_label=task_label,product_id=dd_product_id)
        return
    start_time = time.time()
    try:
        proc_dict[multiprocessing.current_process().pid] = int(time.time())
        result_dic = get_lowest_item_list(device,port,isbn,proc_dict)
        proc_dict[multiprocessing.current_process().pid] = int(time.time())

        if result_dic is None or len(result_dic) <= 0:
            db.insert_account_log(account, ip, port, '33', "最低价获取失败")
        else:
            #插入数据
            db.insert_batch_lowest_price_result(result_dic,task_id,task_label,dd_product_id)
            #更新账号时间戳
            db.update_account_info_date(account)
            #更新账号抓取记录
            db.insert_account_log(account, ip, port, '34', "获取最低价完成")
    except:
        log.error("run_item_lowest exception,port={}".format(port))
        log.error(traceback.format_exc())
        pass
    else:
        go_back(device, 1)
    finally:
        end_time = time.time()
        log.info("run_item_lowest 获取最低价商品结束,product_isbn:{},所用时间:{}".format(product_isbn,str(end_time - start_time)))

def run_items_lowest(device: u2.Device, account, products, task_id, task_label, proc_dict):
    log.info("run_items start port={},size={}".format(account['port'],str(len(products))))
    # 再次进行检测
    app_start_check(device)
    #这里给共享变量赋值一次，防止检测时出现超时，导致中断进程执行
    proc_dict[multiprocessing.current_process().pid] = int(time.time())
    log.info("update proc timestamp port={}".format(account['port']))
    for item in products:
        time_time = time.time()
        run_item_lowest(device=device,ip=account['ip'],port=account['port'],account=account['account'],
                            task_id=task_id,task_label=task_label
                            ,phone=True,product_isbn=item,proc_dict=proc_dict)
        proc_dict[multiprocessing.current_process().pid] = int(time.time())
        log.info("update proc timestamp port={}".format(account['port']))
        log.info("最低价抓取 账号%s-%s抓取%s所用时间 %d" % (account['account'], account['port'], item, (time.time() - time_time)))
    return

def get_memu_policy(account):
    data = db.get_job_status_by_account(account)
    config = json.loads(data['config'])
    log.info("获得账号配置信息:%s", config)
    return config['random']


def run_items(device: u2.Device, account, products, task_id, task_label, proc_dict):
    log.info("run_items start port={},size={}".format(account['port'],str(len(products))))
    # 获取账号动态配置信息
    # random_policy = get_memu_policy(account['account'])
    random_policy = None
    # 再次进行检测
    app_start_check(device)
    #这里给共享变量赋值一次，防止检测时出现超时，导致中断进程执行
    proc_dict[multiprocessing.current_process().pid] = int(time.time())
    log.info("update proc timestamp port={}".format(account['port']))
    for item in products:
        time_time = time.time()
        if '-' in item:
            # 带有skuid，
            item_ids = str.split(item, '-')
            run_item(device, account['ip'], account['port'], account['account'], item_ids[0], random_policy, task_id,
                     task_label, True, item_ids[1])
        else:
            run_item(device, account['ip'], account['port'], account['account'], item, random_policy, task_id,
                     task_label,
                     True, None)
        proc_dict[multiprocessing.current_process().pid] = int(time.time())
        log.info("update proc timestamp port={}".format(account['port']))
        log.info("账号%s-%s抓取%s所用时间 %d" % (account['account'], account['port'], item, (time.time() - time_time)))
    return


def proc_run(account, proc_dict):
    # 0.检查所需的文件目录
    #check_file_path()
    global log
    log = MyLog.Logger(account['port']).get_log()
    # 记录线程，进程信息
    pid = multiprocessing.current_process().pid
    tid = threading.current_thread().ident
    db.insert_account_log(account['account'], account['ip'], account['port'], '30',
                          "pid=%s,tid=%s 进程启动" % (str(pid), str(tid)))
    db.update_job_pid(account['ip'], account['port'], pid)
    db.update_account_status(account['port'], 1)
    # 进程共享变量设置 最新时间
    proc_dict[multiprocessing.current_process().pid] = int(time.time())
    try:
        # 开始启动adb,taobao,postern
        device = time_out_connect(account['port'])
        # 开启检测线程
        thread = threading.Thread(target=check_thread, args=(device, account, proc_dict,))
        thread.setDaemon(True)
        thread.start()
    except:
        log.info("%s 连接失败" % (account['port']))
        db.update_account_status(account['port'], 0)
        raise Exception("%s 连接失败" % (account['port']))
    # app启动，初始化
    app_init(device)
    while True:
        # 共享变量赋值，供主进程进程检测
        proc_dict[multiprocessing.current_process().pid] = int(time.time())
        log.info("update proc timestamp port={}".format(account['port']))
        #获取需要处理的数据
        data = get_task_data(account['port'])
        products = data.get('itemIds',None)
        task_id = data.get('taskId',None)
        task_label =data.get('taskLabel',None)
        task_type = data.get('taskType',None)
        if task_label is None or task_id is None or products is None:
            time.sleep(3)
            continue
        try:
            #根据任务类型执行不同的抓取策略
            if task_type is not None and str(task_type) == '3':
                run_items_lowest(device=device,account=account,products=products,task_id=task_id,task_label=task_label,proc_dict=proc_dict)
            else:
                run_items(device=device, account=account, products=products, task_id=task_id, task_label=task_label,
                          proc_dict=proc_dict)
        except:
            log.info(traceback.format_exc())
            #app 初始化
            app_init(device)
            #异常重启 app
            app_restart(device)
            #app启动检测
            app_start_check(device)
            pass
        else:
            app_start_check(device)


def get_task_data(port):
    get = requests.get("http://192.168.47.230:10003/product/getTaskData?port=%s" % (port))
    #get = requests.get("http://192.168.49.248:10005/product/getTaskData?port=%s" % (port))
    log.info("{port} 请求需要处理的数据 {result}".format(port=port, result=get.text))
    return json.loads(get.text)


def check_thread(device: u2.Device, account, proc_dict):
    while True:
        try:
            # # 关闭下无用弹窗
            close_useless_popup(device)
            # 浮层关闭按钮
            if device.xpath("浮层关闭按钮").exists is True:
                device.xpath("浮层关闭按钮").click()
                db.insert_account_log(account['account'], account['ip'], account['port'], '31', "检测到浮层")
                return
            # 淘金币小镇正在拼命加载中
            if device.xpath("淘金币小镇正在拼命加载中").exists is True:
                device.press("back")
                db.insert_account_log(account['account'], account['ip'], account['port'], '31', "检测到加载淘金币")
                return
            # 赚金币
            if device.xpath("赚金币").exists is True:
                device.press("back")
                db.insert_account_log(account['account'], account['ip'], account['port'], '31', "赚金币")
                return
            # 网络崩溃
            if device.xpath("网络竟然崩溃了").exists is True:
                device.press("back")
                db.insert_account_log(account['account'], account['ip'], account['port'], '31', "网络异常")
                return
            # 检测滑块
            if check_slider(device, account['account'], account['ip'], account['port'], False) is False:
                time.sleep(2)
                return
            # 软件更新
            if device.xpath("软件更新").exists is True and device.xpath("查看详情").exists is True:
                db.insert_account_log(account['account'], account['ip'], account['port'], '31', "系统软件更新提示")
                device.xpath("查看详情").click()
                time.sleep(0.2)
                device.press("back")
                return
            # 屏幕截图
            if proc_dict[multiprocessing.current_process().pid] is not None and (
                    int(time.time()) - proc_dict[multiprocessing.current_process().pid]) > 30:
                img = device.screenshot()
                tmp_time = time.strftime("%Y-%m-%d %H时%M分%S秒 ", time.localtime())
                date = time.strftime("%Y-%m-%d", time.localtime())
                save_path = img_path + date + "\\"  + account['port'] + "\\"
                if os.path.exists(save_path) is False:
                    os.makedirs(save_path)
                imgName = account['port'] + " " + tmp_time + '.png'  # 截图可以单独保存为别的名字的文件
                stringPath = save_path + imgName
                # img.save('filename.png')#图片保存在当前项目的文件夹下边
                img.save(stringPath)  # 保存文件到指定的文件夹下边
        except Exception as e:
            # 检测线程不能停止，出现异常记录日志忽略
            log.info(traceback.format_exc())
            pass
        time.sleep(5)


# 注册退出方法
# atexit.register(main_out_run)
def check_file_path():
    # 检查截屏的目录
    global img_path
    date = time.strftime("%Y-%m-%d", time.localtime())
    temp_img_path = img_path + "\\" + date + "\\"
    exists = os.path.exists(temp_img_path)
    if exists is False:
        os.makedirs(temp_img_path)
    img_path = temp_img_path


if __name__ == '__main__':
    log = MyLog.Logger('CMT').get_log()
    proc_dict = multiprocessing.Manager().dict()
    # 1.查询有效的进程
    account_infos = db.get_account_status(1)
    # 2.kill 正在运行的进程
    kill_exit_proc(account_infos)

    # 3.启动进程
    for account in account_infos:
        db.insert_account_log(account['account'], account['ip'], account['port'], '29', "进程准备启动")
        current_process = multiprocessing.Process(target=proc_run, args=(account, proc_dict,), name=account['port'])
        current_process.start()
    time.sleep(5)
    while True:
        try:
            time.sleep(10)
            # 检测所有的账号有没有全部启动
            accounts = db.get_account_status(1)
            run_adb_code = []
            error_process = []
            for proc in multiprocessing.active_children():
                if 'SyncManager' in proc.name:
                    continue
                try:
                    if proc_dict.get(proc.pid) is None or int(time.time()) - proc_dict.get(proc.pid) >= 60:
                        db.insert_account_log_v2(proc.name, '28', "关闭进程")
                        psutil.Process(proc.pid).kill()
                        proc_dict.pop(proc.pid)
                except:
                    pass
                if proc.is_alive():
                    run_adb_code.append(proc.name)
                    continue
            db.insert_account_v3('32', "进程存活信息信息,主进程:{},子进程:{}".format(multiprocessing.current_process().pid,
                                                                       ','.join(run_adb_code)))
            log.info("run process now,{pid},{run_adb_code}".format(pid=multiprocessing.current_process().pid,
                                                                   run_adb_code=run_adb_code))
            for account in accounts:
                if account['port'] not in run_adb_code:
                    db.insert_account_log(account['account'], account['ip'], account['port'], '29', "进程准备启动")
                    current_process = multiprocessing.Process(target=proc_run, args=(account, proc_dict,),
                                                              name=account['port'])
                    current_process.start()
                    log.info("进程=%s,port=%s 启动成功" % (current_process.pid, current_process.name))
        except:
            log.info(traceback.format_exc())
            pass
