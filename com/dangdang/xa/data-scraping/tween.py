import random

import pyautogui
import math
import random


def sigmoid(n):
    y = n * 10
    noise = random.uniform(0.01,0.02)
    return 1 / (1 + math.exp(-y + 5))+noise


move_tactics = [
    pyautogui.easeInQuad,
    pyautogui.easeOutQuad,
    pyautogui.easeInOutQuad,
    pyautogui.easeInCubic,
    pyautogui.easeOutCubic,
    pyautogui.easeInOutCubic,
    pyautogui.easeInQuart,
    pyautogui.easeOutQuart,
    pyautogui.easeInOutQuart,
    pyautogui.easeInQuint,
    pyautogui.easeOutQuint,
    pyautogui.easeInOutQuint,
    pyautogui.easeInSine,
    pyautogui.easeOutSine,
    pyautogui.easeInOutSine,
    pyautogui.easeInExpo,
    pyautogui.easeOutExpo,
    pyautogui.easeInOutExpo,
    pyautogui.easeInCirc,
    pyautogui.easeOutCirc,
    pyautogui.easeInOutCirc,
    pyautogui.easeInElastic,
    pyautogui.easeOutElastic,
    pyautogui.easeInOutElastic,
    pyautogui.easeInBack,
    pyautogui.easeOutBack,
    pyautogui.easeInOutBack,
    pyautogui.easeInBounce,
    pyautogui.easeOutBounce,
    pyautogui.easeInOutBounce,
    sigmoid
]

def get_tween():
    tween = move_tactics[random.randint(0, len(move_tactics)-1)]
    return tween.__name__,tween
