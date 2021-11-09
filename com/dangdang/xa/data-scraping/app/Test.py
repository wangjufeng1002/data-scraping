import uiautomator2 as u2
import time
def screeon(adb):
    adb.press("back")
    adb.swipe_ext("up", scale=0.9)
    return True
def open_app(adb):
    adb.app_start("com.taobao.taobao")
def check(adb):
    print("出现验证码")
if __name__ == '__main__':
    adb = u2.connect("7ed1fca1")
    adb.app_start("com.taobao.taobao")
    print(adb.app_current().get('package'))
    print(adb.app_info("com.taobao.taobao"))
    print(adb.app_list_running())
    # adb.watcher("首页").when("赚金币").call(lambda d:screeon(adb))
    # adb.watcher.start(1)
    #adb.watcher("1").when("信息").when("拨号").when("浏览器").when("相机").call(lambda d:open_app(adb))
    adb.watcher("check").when("@android:id/decor_content_parent").call(lambda d:check(adb))
    adb.watcher("goldCoins").when("赚金币").press("back")
    adb.watcher.start(1)
    time.sleep(20000)
    # screen = adb.info
    # if screen["screenOn"] == False:  # 屏幕状态
    #     adb.press("power")
    #     adb.swipe_ext("up", scale=0.9)
    #     print("灭屏状态")
    # elif screen["screenOn"] == True:  # 屏幕状态
    #     adb.swipe_ext("up", scale=0.9)
    #     print("亮屏状态")
    # if adb.xpath('//*[@resource-id="com.taobao.taobao:id/searchbtn"]').exists is False:
    #      adb.press("back")
    #running = adb.app_list_running()
    #adb.app_stop("com.taobao.taobao")
    #adb.app_start("com.taobao.taobao")

    #print(running)
    # adb.xpath("@nc_1_n1t").long_click()
    # adb.swipe_ext("right", scale=0.9)
    # adb.xpath(
    #     '//*[@resource-id="com.taobao.taobao:id/sv_search_view"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[5]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]').click()
    # adb.send_keys("哈哈")
    # adb.swipe_points([(165,1356),(945,1470)],0.09)
    # if adb.xpath("nc_1_refresh1").exists is True:
    #     adb.xpath("nc_1_refresh1").click()
    # view__all=  adb.xpath("@com.taobao.taobao:id/rv_main_container").child("//android.widget.HorizontalScrollView").child("//android.widget.TextView").all()
    # for tab in view__all:
    #     print(tab.text)
