import uiautomator2 as u2

if __name__ == '__main__':
    # adb = u2.connect("401fab3")
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
    #view__all=  adb.xpath("@com.taobao.taobao:id/rv_main_container").child("//android.widget.HorizontalScrollView").child("//android.widget.TextView").all()
    # for tab in view__all:
    #     print(tab.text)
    # for i in range(1, 5):
    #     print(i)
    origin_text = "2021-10-14 11:18:18,684-CMT-INFO-进程0账号htc0987282758,获取商品588086971341数据:1/1￥45.56价格￥47.74满49享包邮购买得积分查看큚月销 2Barron's巴朗AP经济学(第6版)(英文版)/SAT\\AP备考书系/出国留学书系 博库网 //gw.alicdn.com/tfs/TB1pwxAr4z1gK0jSZSgXXavwpXa-168-64.png推荐帮我选分享选择配送至:芝罘区큚发货浙江杭州|快递: 5.00큚配送至: 烟台市 芝罘区保障假一赔四 · 极速退款 · 七天无理由退换큚"
    origin_text = origin_text.replace("'", "").replace("\\", "")
    print(origin_text)