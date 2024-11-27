import time
import random
import traceback

import pyautogui
import pyautogui as pag
import requests
import tween
import numpy as np
import logging


if __name__ == '__main__':
    pyautogui.press('win')
    pyautogui.write('chrome')
    pyautogui.press('enter')

    # 等待浏览器打开
    time.sleep(5)