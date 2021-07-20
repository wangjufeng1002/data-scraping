from pymysql_comm import UsingMysql


def get_need_process():
    with UsingMysql() as um:
        um.cursor.execute("select * from item_url  where is_success =0 limit 100")
        data = um.cursor.fetchall()
        return data

def update_status(lists):
    with UsingMysql() as um:
        for item in lists:
            um.cursor.execute("update  item_url set is_success=1  where id="+str(item['id']))
        um._conn.commit()