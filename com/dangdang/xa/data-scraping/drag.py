# 淘宝自动拖动滑块

import time
import random
import pyautogui
import pyautogui as pag
import requests
import tween
import numpy as np
import logging

logging.basicConfig(filename="./logs/draglog.log")


# 噪音随机移动
def noise_remove():
    x = random.uniform(0, 1024)
    y = random.uniform(0, 1024)
    timed = random.uniform(0, 1)
    tweenname, mytween = tween.get_tween()
    print(tweenname)
    pag.moveTo(x, y, duration=timed, tween=mytween)


# 移动到起始点
def move_to_start():
    random.uniform(0, 1025)
    box = get_start_pos()
    timed = random.uniform(0, 1)
    x = box.left + 10 + random.randint(0, 20)
    y = box.top + 10 + random.randint(0, 20)
    tweenname, mytween = tween.get_tween()
    pag.moveTo(x + random.randint(-5, 5), y + random.randint(-5, 5), duration=timed,
               tween=mytween)


def my_drag(x):
    pag.mouseDown(button='left')

    pyautogui.PAUSE = 0.01
    step = random.randint(4, 10)
    num = []
    for i in range(0, step):
        limit = x - np.sum(num)
        start = 10
        if limit < start:
            start = 0
        r = random.randint(start, limit)
        num.append(r)
    num.sort(reverse=True)

    for i in num:
        if i > 0:
            mytweenname, mytween = tween.get_tween()
            print(i, mytweenname)
            pag.moveRel(xOffset=i, yOffset=random.randint(-20, 20), duration=random.uniform(0.07, 0.1), tween=mytween)

    pag.mouseUp(button='left')
    pyautogui.PAUSE = 0.1


def drag():
    timed = random.uniform(0.20, 0.35)
    user = get_user()

    tweenname, mytween = tween.get_tween()
    logging.info("user:" + str(user) + "tween:" + str(tweenname) + "timed:" + str(timed))
    print("user:" + str(user) + "tween:" + str(tweenname) + "timed:" + str(timed))
    pyautogui.dragRel(xOffset=1100 + random.randint(-100, 500), yOffset=random.randint(-20, 20), duration=timed,
                      button='left',
                      tween=mytween)


def scroll():
    if random.randint(0, 1) == 1:
        for i in range(random.randint(0, 3)):
            pag.moveTo(random.randint(0, 1000), random.randint(0, 1000), duration=random.uniform(0.1, 0.2),
                       tween=pyautogui.easeOutQuad)
    pag.moveTo(1017 + random.randint(-20, 20), 662 + random.randint(-20, 20), duration=random.uniform(0.1, 0.2),
               tween=pyautogui.easeOutQuad)
    pyautogui.scroll(-400 + random.randint(100, 200))
    if random.randint(0, 1) == 1:
        for i in range(random.randint(0, 3)):
            offset = random.randint(100, 200)
            pyautogui.scroll(-400 + offset)
            pyautogui.scroll(400 + offset)

    pyautogui.scroll(-400 + random.randint(100, 200))


def get_start_pos():
    return pag.locateOnScreen("start.png", confidence=0.9)


def get_drag_pos():
    box = pag.locateOnScreen("3.png", confidence=0.9)
    print(box)
    return box


def get_user():
    res = requests.get("http://localhost:10001/getInvalidHeader")
    return res.json()


# 900, 836
def get_pos():
    while True:
        x, y = pag.position()
        print(x, y)
        time.sleep(1)


def process():
    time.sleep(1)
    while get_drag_pos() is not None:
        drag()
        time.sleep(1)
        pag.press('f5')
        time.sleep(1)


# 1017,662
# 895,733

if __name__ == '__main__':
    while True:
        if get_drag_pos() is not None:
            # scroll()
            time.sleep(2)
            noise_remove()
            time.sleep(0.1)
            move_to_start()
            if random.randint(0, 1) == 1:
                drag()
            else:
                my_drag(800)
            time.sleep(1)
            pag.press('f5')
