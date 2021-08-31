import uiautomator2 as u2
import time


def test():
    d = u2.connect()  # connect to device
    print(d.info)
    d_app_list = d.app_list()
    # for app in  d_app_list:
    #     print(app+"\n")
    d.app_start("com.tencent.mm")
    d.click(0.666, 0.488)
    for i in range(0,30):
        d.click(0.466, 0.953)
        d.send_keys("鸹貔")
        d.click(0.876, 0.903)
def test2():
    d = u2.connect()  # connect to device
    print(d.info)
    d_app_list = d.app_list()
    # for app in  d_app_list:
    #     print(app+"\n")
    d.app_start("com.tencent.mm")
    d.click(0.876, 0.903)
    for i in range(0,1):
        d.click(0.561, 0.941)
        d.send_keys("还没回呢")
        d.click(0.944, 0.893)
def test3():
    d = u2.connect()  # connect to device
    print(d.info)
    d_app_list = d.app_list()
    # for app in  d_app_list:
    #     print(app+"\n")

    for i in range(0,20):
        d.click(0.345, 0.896)
        d.send_keys("鸹貔")
        d.click(0.944, 0.893)
def taobao():
    d = u2.connect()  # connect to device
    d.app_stop("com.taobao.taobao")
    #d_app_list = d.app_list()
    d.app_start("com.taobao.taobao")
    d.click(0.398, 0.107)
    d.send_keys("http://detail.tmall.com/item.htm?id=39223646642&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4")
    d.click(0.907, 0.061)
    #d(re)
    #print(d_app_list)
def taobao2():
    d = u2.connect("127.0.0.1:21503")
    #d.press("home")
    #d.app_start("com.taobao.taobao"
    d.click(0.333, 0.054)
    d.click(0.277, 0.065)
    d.send_keys("www",clear=True)


if __name__ == '__main__':
    taobao2()