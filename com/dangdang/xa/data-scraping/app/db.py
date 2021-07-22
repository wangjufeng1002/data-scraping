from pymysql_comm import UsingMysql


def get_need_process():
    with UsingMysql() as um:
        um.cursor.execute("select * from book_info  where is_success =0 limit 100")
        data = um.cursor.fetchall()
        return data

def update_status(lists,status):
    with UsingMysql() as um:
        for item in lists:
            um.cursor.execute("update  book_info set is_success="+str(status)+"  where id="+str(item['id']))
        um._conn.commit()