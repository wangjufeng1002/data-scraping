import uiautomator2 as u2
import threading
import time
def get_url():
    adb = u2.connect("e574eade")  # connect to device
    running = adb.app_list_running()
    if "com.taobao.taobao" in running:
        adb.app_stop("com.taobao.taobao")
    adb.app_start("com.taobao.taobao")
    adb.xpath("扫一扫").parent().click()
    adb.send_keys("MySql")
    adb.xpath("搜索").click()
    time.sleep(2)
    layout__all = adb.xpath("com.taobao.taobao:id/libsf_srp_list_root").child("//android.widget.FrameLayout").all()
    for product_label in layout__all:
        product_label.click()
        time.sleep(0.5)
        adb.swipe_ext("up", scale=0.5)  # 代码会vkk
        # time.sleep(0.5)
        # adb.xpath("店铺").click()
        # time.sleep(1)
        # view__all = adb.xpath("__react-content").child("//android.view.View").all()
        # for view in view__all:
        #     print(view.text)
        # adb.press("back")
        # adb.press("back")

        adb.xpath("@com.taobao.taobao:id/uik_public_menu_action_icon").click()
        adb.xpath("复制链接").parent().click()
        clipboard = adb.clipboard
        replace = str.split(clipboard, " ")[1].replace(" ", "")
        print(replace)
def open_browser():
    adb = u2.connect("e574eade")  # connect to device
    running = adb.app_list_running()
    if "com.android.browser" in running:
        adb.app_stop("com.android.browser")
    adb.app_start("com.android.browser")
    xpath = adb.xpath("@com.android.browser:id/a81").wait(1)
    if xpath is not None:
        adb.xpath("@com.android.browser:id/a81").click()
    adb.xpath("@com.android.browser:id/c4u").click()
    adb.send_keys("https://m.tb.cn/h.fd6DVQ1?sm=276e7b")
    adb.xpath("访问").click()
#https://m.tb.cn/h.fd6DVQ1?sm=276e7b
if __name__ == '__main__':
    adb = u2.connect("e574eade")  # connect to device
    running = adb.app_list_running()
    if "com.taobao.taobao" in running:
        adb.app_stop("com.taobao.taobao")
    adb.app_start("com.taobao.taobao")
    adb.xpath("扫一扫").parent().click()
    adb.send_keys("http://detail.tmall.com/item.htm?id=581714396856&rn=7879f011c9d9a0619c97c9897c92684c&abbucket=14")
    adb.xpath("搜索").click()
    time.sleep(1)
    while True:
        adb.swipe_ext("up", scale=0.8)  # 代码会vkk
        time.sleep(1)
        xpath = adb.xpath("参数").exists
        if xpath is True:
            break
    xpath = adb.xpath("参数").click()
    detail_map = {}
    while True:
        container = adb.xpath("@com.taobao.taobao:id/container").all()
        for con in container:
            childs = con.elem.getchildren()
            if len(childs) < 2:
                continue
            key=""
            value=""
            for childEle in childs:
               if childEle.get("resource-id") == 'com.taobao.taobao:id/name' :
                   key = childEle.get("text")
               if childEle.get("resource-id") == 'com.taobao.taobao:id/value':
                   value = childEle.get("text")
            detail_map.setdefault(key,value)
        if detail_map.get("出版社名称") is None:
            adb.swipe_ext("up", scale=0.8)  # 代码会vkk
            time.sleep(0.5)
        else:
            break
    print(detail_map)

def go_back(devices, times):
    for i in range(times):
        devices.press("back")
        time.sleep(0.3)


