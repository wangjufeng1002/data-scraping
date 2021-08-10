from pymysql_comm import UsingMysql
import datetime




def update_info(origin_text,item_id,task_id,task_label):
    with UsingMysql()as um:
        sql = "update product_record set  original_info='{}',`status`=2 where item_id='{}' and task_id='{}' and task_label='{}'".format(origin_text,item_id,task_id,task_label)
        um.cursor.execute(sql)
        um._conn.commit()




def update_account_info(account):
    with UsingMysql() as um:
        sql = "update account_info set `status`=-1  where  account='{}'".format(account)
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
        sql = "update account_info set run_status={} where ip='{}' and port='{}'".format(status, ip, port)
        um.cursor.execute(sql)
        um._conn.commit()

def get_keywords():
    with UsingMysql() as um:
        sql="select key_words from random_keywords"
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def insert_account_log(account,ip,port,action,remark):
    with UsingMysql() as um:
        sql="INSERT INTO account_log (`account`, `ip`, `port`, `action`, `remark`, `create_date`) VALUES ('{}','{}','{}','{}','{}',now())".format(account,ip,port,action,remark)
        um.cursor.execute(sql)
        um._conn.commit()
