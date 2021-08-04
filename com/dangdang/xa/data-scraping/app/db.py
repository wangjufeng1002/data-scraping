from pymysql_comm import UsingMysql
import datetime


def get_need_process():
    with UsingMysql() as um:
        um.cursor.execute("select * from book_info  where is_success =0 limit 100")
        data = um.cursor.fetchall()
        return data


def update_status(lists, status):
    with UsingMysql() as um:
        for item in lists:
            um.cursor.execute("update  book_info set is_success=" + str(status) + "  where id=" + str(item['id']))
        um._conn.commit()


def update_info(origin_text,item_id):
    with UsingMysql()as um:
        sql = "update book_info set original_text='{}',is_success=2 where item_id='{}'".format(origin_text,item_id)
        um.cursor.execute(sql)
        um._conn.commit()


def get_user():
    with UsingMysql()as um:
        # 账号切成2份  一天用一半
        now = datetime.datetime.now()
        mod = now.day % 2
        sql = "select * from headers  where id%2={}  order by update_time asc limit 1".format(mod)
        um.cursor.execute(sql)
        data = um.cursor.fetchone()
        sql = "update headers set update_time=now(),fail_times={} where id={}".format(data['fail_times'] + 1,
                                                                                      data['id'])
        um.cursor.execute(sql)
        um._conn.commit()
        return data


def get_account_info(account):
    with UsingMysql()as um:
        sql = "select * from headers where  account='{}'".format(account)
        um.cursor.execute(sql)
        data = um.cursor.fetchone()
        return data


def update_account_info(account):
    with UsingMysql() as um:
        sql = "update headers set `status`=-1,update_time=now() where  account='{}'".format(account)
        um.cursor.execute(sql)
        um._conn.commit()


def get_job_status(ip, port):
    with UsingMysql() as um:
        sql = "select * from job_status where ip='{}' and port='{}'".format(ip, port)
        um.cursor.execute(sql)
        data = um.cursor.fetchone()
        return data

def get_job_status_by_account(account):
    with UsingMysql() as um:
        sql = "select * from job_status where account='{}'".format(account)
        um.cursor.execute(sql)
        data = um.cursor.fetchone()
        return data
def update_job_status(ip, port, status):
    with UsingMysql() as um:
        sql = "update job_status set run_status={} where ip='{}' and port='{}'".format(status, ip, port)
        um.cursor.execute(sql)
        um._conn.commit()
