import threading
import time
import traceback

import db
from datetime import datetime


def check():
    while True:
        try:
            accounts = db.get_running_account()
            for account in accounts:
                now = datetime.now()
                delta = now - account['last_modified_time']
                print("账号{}最后更新时间是{}".format(account['account'], account['last_modified_time']))
                if delta.total_seconds() > 200:
                    print("账号{},最后更新时间超过600秒,置为未运行状态".format(account['account']))
                    db.init_run_status(account['account'])
            time.sleep(30)
        except Exception:
            print(traceback.format_exc())


if __name__ == '__main__':
    check()