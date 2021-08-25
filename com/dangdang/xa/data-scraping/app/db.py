from pymysql_comm import UsingMysql
import datetime


def update_info(origin_text, item_id, task_id, task_label):
    with UsingMysql()as um:
        sql = "update product_record set  original_info='{}',`status`=2 where item_id='{}' and task_id='{}' and task_label='{}'".format(
            origin_text, item_id, task_id, task_label)
        um.cursor.execute(sql)
        um._conn.commit()


def get_running_account():
    with UsingMysql() as um:
        sql = "select * from account_info where run_status='1'"
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def update_account_info(account):
    with UsingMysql() as um:
        sql = "update account_info set `status`=-1 ,next_deal_time=now()  where  account='{}'".format(account)
        um.cursor.execute(sql)
        um._conn.commit()


def init_run_status(account):
    with UsingMysql() as um:
        sql = "update account_info set run_status='0' ,last_modified_time=now() where  account='{}'".format(account)
        um.cursor.execute(sql)
        um._conn.commit()


def update_account_info_date(account):
    with UsingMysql() as um:
        sql = "update account_info set last_modified_time=now()  where  account='{}'".format(account)
        um.cursor.execute(sql)
        um._conn.commit()


def get_job_status(ip, port):
    with UsingMysql() as um:
        sql = "select * from account_info where ip='{}' and port='{}'".format(ip, port)
        um.cursor.execute(sql)
        data = um.cursor.fetchone()
        return data


def get_job_status_by_account(account):
    with UsingMysql() as um:
        sql = "select * from account_info where account='{}'".format(account)
        um.cursor.execute(sql)
        data = um.cursor.fetchone()
        return data


def update_job_status(ip, port, status):
    with UsingMysql() as um:
        sql = "update account_info set run_status={},last_modified_time=now() where ip='{}' and port='{}'".format(
            status, ip, port)
        um.cursor.execute(sql)
        um._conn.commit()


def get_keywords():
    with UsingMysql() as um:
        sql = "select key_words from random_keywords"
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def insert_account_log(account, ip, port, action, remark):
    with UsingMysql() as um:
        sql = "INSERT INTO account_log (`account`, `ip`, `port`, `action`, `remark`, `create_date`) VALUES ('{}','{}','{}','{}','{}',now())".format(
            account, ip, port, action, remark)
        um.cursor.execute(sql)
        um._conn.commit()


def get_cookies():
    with UsingMysql() as um:
        sql = "select * from cookies"
        um.cursor.execute(sql)
        return um.cursor.fetchone()


def get_url_by_shop_name(shop_name):
    with UsingMysql() as um:
        sql ="select search_url from shop_url where shop_name='{}'".format(shop_name)
        um.cursor.execute(sql)
        return um.cursor.fetchone()

def get_book_url(id):
    with UsingMysql() as um:
        sql="select item_id from item_url where item_id='{}'".format(id)
        um.cursor.execute(sql)
        return um.cursor.fetchone()

def insert_book_url(url,id,shop):
    with UsingMysql()as um:
        sql = "insert into item_url(`item_url`,`item_id`,`shop_name`,`create_time`,`update_time`,`is_success`)value ('{}','{}','{}',now(),now(),0)".format(url,id,shop)
        um.cursor.execute(sql)
        um._conn.commit()
