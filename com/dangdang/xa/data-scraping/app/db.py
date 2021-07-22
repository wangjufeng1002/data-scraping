from pymysql_comm import UsingMysql


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
        sql="update book_info set  default_price='{}',active_price='{}',coupons='{}',free='{}',original_text='{}',sales='{}',is_success=2 where item_id='{}'".format(
                data.defaultPrice, data.activePrice, data.coupons, data.free, data.originalText, data.sales, data.itemId)
        print(sql)
        um.cursor.execute(sql)
        um._conn.commit()
