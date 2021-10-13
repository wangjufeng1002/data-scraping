import uiautomator2 as u2

if __name__ == '__main__':
    adb = u2.connect("e4b1eae1")
    webWiew = adb.xpath("//android.webkit.WebView").all()
    for w in webWiew:
        if "金币小镇-首页" in w.text:
            adb.press("back")