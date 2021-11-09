import threading
import multiprocessing
import time
from multiprocessing.connection import Connection

import psutil
import setproctitle

def thread_method():
    print(multiprocessing.current_process().pid)
    print(str(threading.current_thread().ident) + "-" +threading.current_thread().name+ " 线程开始 "+ time.strftime("%Y-%m-%d %H:%M:%S"))
    ps =[]
    for i in range(1,3):
        p = multiprocessing.Process(target=process_method, args=(),name="测试进程名称-"+str(i))
        p.start()
        ps.append(p)
    time.sleep(5)
    for p in ps:
        p.join()
    print("线程结束"+time.strftime("%Y-%m-%d %H:%M:%S"))


def process_method():
    setproctitle.setproctitle("test")
    print(setproctitle.getproctitle())
    print(multiprocessing.current_process().name+" 进程开始执行"+time.strftime("%Y-%m-%d %H:%M:%S") + " pid= "+str(multiprocessing.current_process().pid))
    time.sleep(20000)
    print(multiprocessing.current_process().name+" 进程结束执行"+time.strftime("%Y-%m-%d %H:%M:%S"))

def send_proc(out_pip:Connection):
    for i in range(1,30):
        out_pip.send(i)
        time.sleep(1)


if __name__ == '__main__':
    # print(multiprocessing.current_process().pid)
    # print("main========================")
    # t = threading.Thread(target=thread_method, args=())
    # t.start()
    # t.join()
    out_pip,in_pip = multiprocessing.Pipe(True)
    multiprocessing.Process(target=send_proc,args=(out_pip,)).start()
    time.sleep(10)
    while True:
        print(in_pip.recv())


