
import uiautomator2 as u2
import time


#http://192.168.47.230:10003/product/getTaskData?port=%s

def collect(urls):
    # 8daff499  178061ed
    d = u2.connect("178061ed")
    d.app_start("com.taobao.taobao")

    num = 0
    for url in lines:
        num = num+1
        # 回到首页
        while d.xpath("推荐").exists is False or d.xpath("扫一扫").exists is False or d.xpath("搜索").exists is False:
            if d.xpath("首页").exists is True:
                d.xpath("首页").click()
                d.xpath("推荐").click()
            else:
                for i in range(1):
                    d.press("back")
                d.xpath("首页").wait(0.1)
        # 点解搜索
        d.xpath('//*[@resource-id="com.android.systemui:id/wifi_combo"]').click()
        d.click(0.257, 0.121)
        d.click(0.343, 0.05)
        # 搜索单品
        d.send_keys(url)
        d.xpath("搜索").click_exists()
        d.xpath("收藏").click_exists()
        print("do {} done:{}".format(num, url))


if __name__ == '__main__':

    # 获取数据
    textFile = open(r'D:\桌面\itemUrl.txt')
    lines = textFile.readlines()
    textFile.close()

    collect(lines)
    print("done..............")



