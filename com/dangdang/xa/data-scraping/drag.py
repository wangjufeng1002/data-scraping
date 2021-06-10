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


def drag():
    if random.randint(0, 1) == 1:
        for i in range(random.randint(0, 3)):
            pag.moveTo(random.randint(0, 1000), random.randint(0, 1000), duration=random.uniform(0.1, 0.2),
                       tween=pyautogui.easeOutQuad)
    pag.moveTo(895 + random.randint(-5, 5), 733 + random.randint(-5, 5), duration=random.uniform(0.1, 0.2),
               tween=pyautogui.easeOutQuad)
    timed = random.uniform(0.2, 0.3)

    eases = [
        pyautogui.easeOutQuad,  # 0.2-0.3
        pyautogui.easeInOutQuad,
    ]
    chose = random.randint(0, 1)
    if chose == 1:
        dragTo(900 + random.randint(-5, 500))
    else:
        pyautogui.dragRel(xOffset=900 + random.randint(-5, 500), yOffset=random.randint(-5, 5), duration=timed,
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
    box = pag.locateOnScreen("2.png", confidence=0.9)
    print(box)
    return box


# 1017,662
# 895,733
noneIndex = 0
if __name__ == '__main__':
    while True:
        if noneIndex > 20:
            pag.press('f5')

            noneIndex = 0
        if get_drag_pos() is not None:
            noneIndex = 0
            time.sleep(random.uniform(0.5, 1.5))
            scroll()
            drag()
            time.sleep(random.uniform(0.5, 1.5))
            pag.press('f5')
        else:
            noneIndex = noneIndex + 1
        time.sleep(1)

        if random.randint(0, 1) == 1:
            pag.moveTo(random.randint(0, 1000), random.randint(0, 1000), duration=random.uniform(0.1, 0.2),
                       tween=pyautogui.easeOutQuad)
