# 淘宝自动拖动滑块

import time
import random
import pyautogui
import pyautogui as pag


def dragTo(x):
    pag.mouseDown()
    for i in range(5):
        pag.moveRel(x - random.randint(300, 500), random.randint(-5, 5))
    pag.mouseUp()


def myEaseOutQuad(n):
    res =-n * (n - 2)
    noise=random.randint(-5,5)
    return res +noise

def myeaseInOutQuad(n):
    noise = random.randint(-5, 5)
    if n < 0.5:
        return 2 * n**2+noise
    else:
        n = n * 2 - 1
        return -0.5 * (n*(n-2) - 1)+noise
def drag():
    if random.randint(0, 1) == 1:
        for i in range(random.randint(0, 3)):
            pag.moveTo(random.randint(0, 1000), random.randint(0, 1000), duration=random.uniform(0.1, 0.2),
                       tween=pyautogui.easeOutQuad)
    pag.moveTo(903 + random.randint(-5, 5), 813 + random.randint(-5, 5), duration=random.uniform(0.1, 0.2),
               tween=pyautogui.easeOutQuad)
    timed = random.uniform(0.2, 0.3)

    eases = [
        myEaseOutQuad,  # 0.2-0.3
        myeaseInOutQuad,
    ]
    chose = random.randint(0, 1)
    if chose == 1:
        dragTo(1100 + random.randint(-5, 500))
    else:
        pyautogui.dragRel(xOffset=1100 + random.randint(-5, 500), yOffset=random.randint(-5, 5), duration=timed,
                          button='left',
                          tween=eases[0])


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


def get_drag_pos():
    box = pag.locateOnScreen("3.png", confidence=0.9)
    print(box)
    return box

# 900, 836
def get_pos():
    while True:
        x,y =pag.position()
        print(x,y)
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
            scroll()
            drag()
            time.sleep(1)
            pag.press('f5')
        time.sleep(1)
