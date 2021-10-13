import uiautomator2 as u2

if __name__ == '__main__':
    adb = u2.connect("7be1f4a9")
    running = adb.app_list_running()
    adb.app_stop("com.taobao.taobao")
    adb.app_start("com.taobao.taobao")

    #print(running)
    # adb.xpath("@nc_1_n1t").long_click()
    # adb.swipe_ext("right", scale=0.9)
    adb.xpath('//*[@content-desc="搜索栏"]').click()
    adb.send_keys("哈哈")
    # adb.swipe_points([(165,1356),(945,1470)],0.09)
    # if adb.xpath("nc_1_refresh1").exists is True:
    #     adb.xpath("nc_1_refresh1").click()
