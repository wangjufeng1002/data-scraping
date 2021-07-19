import uiautomator2 as u2
import time
import cv2


def get_item(devices):
    items = devices(className="android.support.v7.widget.RecyclerView",
                    resourceId="com.taobao.taobao:id/libsf_srp_header_list_recycler").child(className="android.widget.LinearLayout")
    index=0
    while index<items.count:
        items[index].click()
        time.sleep(0.5)
        get_item_detail(devices)
        devices.press("back")
        index+=3



def get_buy_content(devices):
    page_item = devices(className="android.widget.LinearLayout",
                        resourceId="com.taobao.taobao:id/ll_bottom_bar").child()
    for item in page_item:
        print(item.info)


def click_search(devices,name):
    d.set_fastinput_ime(True)
    devices.click(300, 150)
    time.sleep(1)
    devices.send_keys(name)
    devices.send_action("search")


def get_item_detail(devices):
    content = ''
    page_item = devices(className="android.widget.ListView",
                        resourceId="com.taobao.taobao:id/mainpage").child(className="android.widget.TextView")
    for item in page_item:
        if item.get_text() != '':
            content += item.get_text()
    print(content)
    return content



# com.taobao.taobao
if __name__ == '__main__':
    d = u2.connect()

    book=[
        "http://detail.tmall.com/item.htm?id=39223646642&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=626388285508&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=16726196775&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=575251404997&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=633437611223&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=23959976662&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=598828568845&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=564347140379&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=556895406356&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=609006074501&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=565099320695&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=527840727428&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=565909682922&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=522853890777&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=647399600482&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=622656833846&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=577094962015&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=603655660665&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=625238200043&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=42007945926&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=569474707008&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=10830460172&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=642179571277&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=625147774117&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=634468055850&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=39154613691&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=10912235136&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=571818112047&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=40495412397&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=611293999811&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=605894101493&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=37335456292&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=553943215038&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=530619758233&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=553114784443&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=647862077380&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=645300798545&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=571932808185&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=541462116798&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=606178721616&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
        "http://detail.tmall.com/item.htm?id=625467713659&rn=bf83a14e4dcf60aafb7fdf279450a057&abbucket=4",
    ]
    for b in book:
        click_search(d,b)
        time.sleep(1)
        get_item_detail(devices=d)
        time.sleep(1)
        d.press("back")
        time.sleep(1)
        d.press("back")
        time.sleep(1)
        d.press("back")

