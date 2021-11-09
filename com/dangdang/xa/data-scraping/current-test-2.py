import os
import threading
import multiprocessing
import time
import psutil
import setproctitle

if __name__ == '__main__':
   print(setproctitle.getthreadtitle())
   print(psutil.Process(7404))