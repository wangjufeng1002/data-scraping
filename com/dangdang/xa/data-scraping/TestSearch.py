import uiautomator2 as u2
import threading
import time
if __name__ == '__main__':
    adb = u2.connect("e574eade")  # connect to device
    running = adb.app_list_running()
    if "com.taobao.taobao" in running:
        adb.app_stop("com.taobao.taobao")
    adb.app_start("com.taobao.taobao")
    adb.xpath("扫一扫").parent().click()
    adb.send_keys("Netty")
    adb.xpath("搜索").click()
    time.sleep(2)
    layout__all = adb.xpath("com.taobao.taobao:id/libsf_srp_list_root").child("//android.widget.FrameLayout").all()
    for product_label in layout__all:
        product_label.click()
        adb.swipe_ext("up", scale=0.5)  # 代码会vkk
        adb.xpath("店铺").click()
        time.sleep(1)
        view__all = adb.xpath("__react-content").child("//android.view.View")
        print(view__all)

