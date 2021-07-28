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


def update_info(data):
    with UsingMysql()as um:
        sql = "update book_info set  default_price='{}',active_price='{}',coupons='{}',free='{}',original_text='{}',sales='{}',is_success=2 where item_id='{}'".format(
            data.defaultPrice, data.activePrice, data.coupons, data.free, data.originalText, data.sales, data.itemId)
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

