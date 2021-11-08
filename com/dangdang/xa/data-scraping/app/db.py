from pymysql_comm import UsingMysql
import datetime


def update_info(origin_text, item_id, task_id, task_label,sku):
    origin_text= origin_text.replace("'","").replace("\\","")
    with UsingMysql()as um:
        if sku is not None:
            sql = "update product_record set  original_info='{}',`status`=2 where item_id='{}'and sku_id='{}' and task_id='{}' and task_label='{}' and status=1".format(
                origin_text, item_id,sku, task_id, task_label)
        else:
            sql = "update product_record set  original_info='{}',`status`=2 where item_id='{}' and task_id='{}' and task_label='{}' and status=1".format(
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
def update_job_status_lock(ip, port, status):
    with UsingMysql() as um:
        sql = "update account_info set run_status={},last_modified_time=now() where ip='{}' and port='{}' and run_status !={}".format(
            status, ip, port,status)
        um.cursor.execute(sql)
        um._conn.commit()
        return um.cursor.rowcount

def update_job_pid(ip,port,pid):
    with UsingMysql() as um:
        sql = "update account_info set pid={},last_modified_time=now() where ip='{}' and port='{}' ".format(
            pid, ip, port)
        um.cursor.execute(sql)
        um._conn.commit()
        return um.cursor.rowcount

def get_keywords():
    with UsingMysql() as um:
        sql = "select key_words from random_keywords"
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def insert_account_log(account, ip, port, action, remark):
    account_info=get_job_status(ip,port)
    proxy=account_info['proxy_ip']
    with UsingMysql() as um:
        sql = "INSERT INTO account_log (`account`, `ip`, `proxy_ip`,`port`, `action`, `remark`, `create_date`) VALUES ('{}','{}','{}','{}','{}','{}',now())".format(
            account, ip, proxy,port, action, remark)
        um.cursor.execute(sql)
        um._conn.commit()


def get_cookies():
    with UsingMysql() as um:
        sql = "select * from cookies where `status`=1  order  by update_time asc "
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def update_cookies_status(status, id):
    with UsingMysql() as um:
        sql = "update cookies set update_time=now(),`status`='{}' where id='{}'".format(status,id)
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_url_by_shop_name(shop_name):
    with UsingMysql() as um:
        sql = "select search_url from shop_url where shop_name='{}'".format(shop_name)
        um.cursor.execute(sql)
        return um.cursor.fetchone()


def get_book_url(id):
    with UsingMysql() as um:
        sql = "select item_id from item_url where item_id='{}'".format(id)
        um.cursor.execute(sql)
        return um.cursor.fetchone()


def insert_book_url(url, id, shop):
    with UsingMysql()as um:
        sql = "insert into item_url(`item_url`,`item_id`,`shop_name`,`create_time`,`update_time`,`is_success`)value ('{}','{}','{}',now(),now(),0)".format(
            url, id, shop)
        um.cursor.execute(sql)
        um._conn.commit()

def get_book_url_by_status(status):
    with UsingMysql() as um:
        sql = "select item_id,item_url,shop_name from item_url where is_success='{}' limit 10".format(status)
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def insert_book_data(book):
    with UsingMysql() as um:
        sql = "INSERT INTO `data_scraping`.`book`" \
              " ( `tm_id`, `book_name`, `book_isbn`, `book_auther`, `book_price`, `book_fix_price`, `book_prom_price`, `book_prom_price_desc`, " \
              "`book_active_desc`, `shop_name`,`book_prom_type`,`book_active_start_time`,`book_active_end_time`,`category`,`book_sales`,`book_press`,`sku_id`,`sku_name`) " \
              "VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s') " \
              "ON DUPLICATE KEY " \
              "UPDATE " \
              "book_name= '%s' " \
              ", book_isbn= '%s' " \
              ", book_auther = '%s' " \
              ", book_price = '%s'" \
              ", book_fix_price = '%s'" \
              ", book_prom_price = '%s'" \
              ", book_prom_price_desc = '%s'" \
              ", book_active_desc = '%s'" \
              ", shop_name = '%s'" \
              ", book_prom_type = '%s'" \
              ", book_active_start_time = '%s'" \
              ", book_active_end_time = '%s'" \
              ", category = '%s'" \
              ", book_sales = '%s'" \
              ", book_press = '%s'" \
              ", sku_id = '%s' " \
              ", sku_name = '%s' " \
              % (book.getTmId(), book.getName(), book.getIsbn(), book.getAuther(), book.getPrice(), book.getFixPrice(),
                 book.getPromotionPrice(), book.getPromotionPriceDesc(), book.getActiveDescStr(), book.getShopName(),
                 book.getPromotionType(), book.getActiveStartTime(), book.getActiveEndTime(), book.getCategory(),
                 book.getSales(), book.getPress(), book.getSkuId(), book.getSkuName(),

                 book.getName(), book.getIsbn(), book.getAuther(), book.getPrice(), book.getFixPrice(),
                 book.getPromotionPrice(), book.getPromotionPriceDesc(), book.getActiveDescStr(), book.getShopName(),
                 book.getPromotionType(), book.getActiveStartTime(), book.getActiveEndTime(), book.getCategory(),
                 book.getSales(), book.getPress(), book.getSkuId(), book.getSkuName(),
                 )
        um.cursor.execute(sql)
        um._conn.commit()

def update_item_url_status(status,item_id):
    with UsingMysql() as um:
        sql = "update  item_url set is_success='{}'  where item_id ='{}' ".format(status,item_id)
        um.cursor.execute(sql)
        um._conn.commit()

def get_account_status(status):
    with UsingMysql() as um:
        sql = "select * from account_info where status='{}'".format(status)
        um.cursor.execute(sql)
        return um.cursor.fetchall()

def get_account_port(port):
    with UsingMysql() as um:
        sql = "select * from account_info where port='{}'".format(port)
        um.cursor.execute(sql)
        return um.cursor.fetchone()
def update_account_status( port, status):
    with UsingMysql() as um:
        sql = "update account_info set run_status={},last_modified_time=now() where  port='{}'".format(
            status, port)
        um.cursor.execute(sql)
        um._conn.commit()

def update_record_info(origin_text, item_id, task_id, task_label,sku):
    origin_text= origin_text.replace("'","").replace("\\","")
    with UsingMysql()as um:
        if sku is not None:
            sql = "update product_record set  original_info='{}',`status`=2 where item_id='{}'and sku_id='{}' and task_id='{}' and task_label='{}'".format(
                origin_text, item_id,sku, task_id, task_label)
        else:
            sql = "update product_record set  original_info='{}',`status`=2 where item_id='{}' and task_id='{}' and task_label='{}'".format(
                origin_text, item_id, task_id, task_label)
        um.cursor.execute(sql)
        um._conn.commit()
