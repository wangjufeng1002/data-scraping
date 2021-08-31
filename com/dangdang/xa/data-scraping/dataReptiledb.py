#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
import pandas as pd
from entity import Book, ItemUrl, Logger, Header
import threading
from dbConnectPool import POOL

bookLock = threading.Lock()
itemUrlLock = threading.Lock()
headerLock = threading.Lock()

host = None
logUtils = None
conn = None
defaultHost = "192.168.47.210"


def init(hostParam, logFile):
    global logUtils
    global conn
    global host
    if hostParam is None:
        host = defaultHost
    else:
        host=hostParam
    logUtils = Logger(filename=logFile, level='info')
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")


# host="127.0.0.1"

def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


def getHeaders(account):
    headers = []
    try:
        conn = POOL.connection()
        cursor = conn.cursor()
        if account is not None:
            execute = cursor.execute(
                "select `cookie`,`referer`,`user-agent`,`account`,`status` from headers where account='%s' " % account)
        else:
            execute = cursor.execute("select `cookie`,`referer`,`user-agent`,`account`,`status` from headers ")
        result = cursor.fetchall()
        description = cursor.description
        columns = []
        for i in range(len(description)):
            columns.append(description[i][0])  # 获取字段名，咦列表形式保存
        for i in range(len(result)):
            head = {}
            # 取出每一行 和 列名组成map
            row = list(result[i])
            for j in range(len(columns)):
                head[columns[j]] = row[j]
            headers.append(head)
        cursor.close()
        conn.commit()
        return headers
    except:
        conn.rollback()
        return headers
    finally:
        conn.close()


def insertDetailPrice(book):
    conn = POOL.connection()
    cursor = conn.cursor()
    sql = "INSERT INTO `data-scraping`.`book`" \
          " ( `tm_id`, `book_name`, `book_isbn`, `book_auther`, `book_price`, `book_fix_price`, `book_prom_price`, `book_prom_price_desc`, " \
          "`book_active_desc`, `shop_name`,`book_prom_type`,`book_active_start_time`,`book_active_end_time`,`category`,`book_sales`,`book_press`) " \
          "VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s') " \
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
          % (book.getTmId(), book.getName(), book.getIsbn(), book.getAuther(), book.getPrice(), book.getFixPrice(),
             book.getPromotionPrice(), book.getPromotionPriceDesc(), book.getActiveDescStr(), book.getShopName(),
             book.getPromotionType(), book.getActiveStartTime(), book.getActiveEndTime(), book.getCategory(),
             book.getSales(), book.getPress(),

             book.getName(), book.getIsbn(), book.getAuther(), book.getPrice(), book.getFixPrice(),
             book.getPromotionPrice(), book.getPromotionPriceDesc(), book.getActiveDescStr(), book.getShopName(),
             book.getPromotionType(), book.getActiveStartTime(), book.getActiveEndTime(), book.getCategory(),
             book.getSales(), book.getPress()
             )
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logUtils.logger.error("数据库插入Price发生异常{itemId}".format(itemId=book.getTmId()))
        logUtils.logger.error("数据库插入Price发生异常 {}", e)
        conn.rollback()
    finally:
        conn.close()


def insertIp(ip):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "INSERT INTO `data-scraping`.`ip_pool` (`ip`) VALUES ('%s') ON DUPLICATE KEY UPDATE ip = '%s'" % (ip, ip)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("数据库插入ip发生异常 {}", e)
        conn.rollback()
    finally:
        cursor.close()


def insertIps(ips):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    sql = "INSERT INTO `data-scraping`.`ip_pool` (`ip`) VALUES ('%s') ON DUPLICATE KEY UPDATE ip = ip"
    cursor = conn.cursor()
    for ip in ips:
        exeSql = sql % ip
        try:
            cursor.execute(exeSql)
            conn.commit()
        except Exception as e:
            print("数据库插入ip发生异常 {}", e)
            conn.rollback()
    cursor.close()


def getIpList():
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "select ip from `ip_pool`"
    try:
        cursor.execute(sql)
        fetchall = cursor.fetchall()
        ips = []
        for ip in list(fetchall):
            try:
                ips.append(ip[0])
            except:
                print("异常ip %s" % ip)
        return ips
    except Exception as e:
        print("查询ip发生异常 {}", e)
    finally:
        cursor.close()


def insertItemUrl(itemUrls):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "INSERT INTO `data-scraping`.`item_url` ( `item_id`, `item_url`, `shop_name`,`category`) VALUES ( '%s', '%s', '%s','%s')" \
          " ON DUPLICATE KEY UPDATE item_id = '%s' ,item_url = '%s',shop_name = '%s',category = '%s' "

    for itemUrl in itemUrls:
        exeSql = sql % (
            itemUrl.itemId, itemUrl.itemUrl, itemUrl.shopName, itemUrl.category, itemUrl.itemId, itemUrl.itemUrl,
            itemUrl.shopName,
            itemUrl.category
        )
        try:
            cursor.execute(exeSql)
            conn.commit()
        except Exception as e:
            print("数据库插入 item_url 发生异常 {}", e)
            conn.rollback()
    cursor.close()


def getItemUrl(category ,page_size,startId,endId):
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        if page_size is None:
            page_size = 1000
        sql = "select item_id as itemId,item_url as itemUrl,shop_name as shopName ,category from `item_url` where  category='%s' and id >='%s' and id <='%s' and is_success !=1 and is_success !=100 order by update_time ASC limit %d"
        e_sql = sql % (category,str(startId), str(endId),page_size)
        execute = cursor.execute(e_sql)
        if execute <= 0:
            return None
        result = cursor.fetchall()
        description = cursor.description
        columns = []
        itemUrlObjs = []
        for i in range(len(description)):
            columns.append(description[i][0])  # 获取字段名，咦列表形式保存
        for i in range(len(result)):
            itemUrl = {}
            itemUrlObj = ItemUrl(itemId=None, itemUrl=None, shopName=None, category=None)
            # 取出每一行 和 列名组成map
            row = list(result[i])
            for j in range(len(columns)):
                itemUrl[columns[j]] = row[j]
            dict2obj(itemUrlObj, itemUrl)
            itemUrlObjs.append(itemUrlObj)
        return itemUrlObjs
    finally:
        cursor.close()
        conn.close()


def updateBookSuccessFlag(flag, itemId):
    conn = POOL.connection()
    cursor = conn.cursor()
    sql = "update  `book` set is_success = %d where tm_id = '%s' " % (flag, itemId)
    try:
        execute = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logUtils.logger.error("更新 book.is_success {itemId}失败".format(itemId=itemId))
        raise e
    finally:
        cursor.close()
        conn.close()
    if execute <= 0:
        return False
    else:
        return True


def updateSuccessFlag(flag, itemId):
    if itemUrlLock.acquire():
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        sql = "update  `item_url` set is_success = %d where item_id = '%s' " % (flag, itemId)
        try:
            execute = cursor.execute(sql)
            conn.commit()
        except Exception as e:
            cursor.close()
            print("更新 item_url 失败")
            raise e
        finally:
            itemUrlLock.release()
            cursor.close()
        if execute <= 0:
            return False
        else:
            return True


def getPageIndex(page, shopId, isSuccess):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "select page_index  from `page_record` where  page_index = %d and shop_id = %d and is_success = %d"
    cursor.execute(sql % (page, shopId, isSuccess))
    fetchall = cursor.fetchall()
    pageIndex = []
    for page in list(fetchall):
        try:
            pageIndex.append(page[0])
        except:
            print("page_index %s" % page)
    return pageIndex


def getPageRecords(shopId, isSuccess, category):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "select page_index  from `page_record` where  shop_id = %d and is_success = %d and category ='%s'"
    cursor.execute(sql % (shopId, isSuccess, category))
    fetchall = cursor.fetchall()
    pageIndex = []
    for page in list(fetchall):
        try:
            pageIndex.append(page[0])
        except:
            print("page_index %s" % page)
    return pageIndex


def updatePageRecords(page, shopId, isSuccess, category):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "update `page_record` set is_success = %d  where page_index = %d and shop_id = %d and category='%s'"
    cursor.execute(sql % (isSuccess, page, shopId, category))
    conn.commit()
    cursor.close()


def updatePageRecordsBatch(page, shopId, isSuccess, category):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "update `page_record` set is_success = %d  where page_index = %d and shop_id = %d and category='%s'"

    for tempPage in page:
        cursor.execute(sql % (isSuccess, tempPage, shopId, category))

    conn.commit()
    cursor.close()


def insertPageIndex(page, shopId, isSuccess, category):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    sql = "insert into `page_record`(page_index,shop_id,is_success,category) values(%d,%d,%d,'%s')"
    cursor = conn.cursor()
    cursor.execute(sql % (page, shopId, isSuccess, category))
    conn.commit()
    cursor.close()


def getNotDealCategory():
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    sql = "select DISTINCT category  as category from item_url where is_success !=1 and  category is not NULL"
    cursor = conn.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    categorys = []
    for category in list(fetchall):
        try:
            categorys.append(category[0])
        except Exception as e:
            print(e)
    return categorys


def getNotDealCategoryByBook():
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    # sql = "select DISTINCT category  as category from book where (book_prom_type is null or book_prom_type = '无' or book_prom_type = 'NULL') and   category is not NULL"
    sql = "select DISTINCT category  as category from book where is_success =0  and   category is not NULL"
    cursor = conn.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    categorys = []
    for category in list(fetchall):
        try:
            categorys.append(category[0])
        except Exception as e:
            print(e)
    return categorys

def getNotDealCategoryByItemUrl(startId,endId):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    # sql = "select DISTINCT category  as category from book where (book_prom_type is null or book_prom_type = '无' or book_prom_type = 'NULL') and   category is not NULL"
    if id is not None:
        sql = "select DISTINCT category  as category from item_url where is_success <=0 and  category is not NULL and id >= {startId} and id <= {endId}".format(startId=startId,endId=endId)
    else:
        sql = "select DISTINCT category  as category from item_url where is_success <=0 and  category is not NULL"
    cursor = conn.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    categorys = []
    for category in list(fetchall):
        try:
            categorys.append(category[0])
        except Exception as e:
            print(e)
    return categorys


def getBookByNotHavePromo(category, size):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    sql = '''select tm_id as tmId,
			 book_name as name,
			 book_isbn as isbn,
			 book_auther as auther,
			 book_price as price,
			 book_fix_price as fixPrice,
			 book_prom_price as promotionPrice,
			 book_prom_price_desc as promotionPriceDesc,
			 book_prom_type as promotionType,
			 book_active_desc as activeDesc,
			 book_active_start_time as activeStartTime,
			 book_active_end_time as activeEndTime,
			 shop_name as shopName,
			 category as category,
			 book_sales as sales,
			 book_press as press
             from book where  category = '%s' 
             and is_success != 1 and is_success != 2
             order by update_time ASC
             limit %d '''
    cursor = conn.cursor()
    cursor.execute(sql % (category, size))
    result = cursor.fetchall()
    description = cursor.description
    columns = []
    bookObjs = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        bookMap = {}
        book = Book(tmId=None, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                    promotionPriceDesc=None, price=None, promotionType=None, activeStartTime=None,
                    activeEndTime=None,
                    activeDesc="", shopName=None, category=None, sales="0",
                    press=None)
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            bookMap[columns[j]] = row[j]
        dict2obj(book, bookMap)
        bookObjs.append(book)
    return bookObjs


def getItemUrlByShopName(shopName, size):
    conn = pymysql.connect(host=host, port=3306, user="root", password="123456", database="data-scraping",
                           charset="utf8")
    cursor = conn.cursor()
    sql = "select item_id as itemId,item_url as itemUrl,shop_name as shopName ,category from `item_url` where  shop_name='%s' and is_success !=1 and is_success !=100 order by update_time ASC limit %d"
    execute = cursor.execute(sql % (shopName, size))
    if execute <= 0:
        return None
    result = cursor.fetchall()
    description = cursor.description
    columns = []
    itemUrlObjs = []
    for i in range(len(description)):
        columns.append(description[i][0])  # 获取字段名，咦列表形式保存
    for i in range(len(result)):
        itemUrl = {}
        itemUrlObj = ItemUrl(itemId=None, itemUrl=None, shopName=None, category=None)
        # 取出每一行 和 列名组成map
        row = list(result[i])
        for j in range(len(columns)):
            itemUrl[columns[j]] = row[j]
        dict2obj(itemUrlObj, itemUrl)
        itemUrlObjs.append(itemUrlObj)
    return itemUrlObjs


def updateHeaders(header):
    sql = "update headers set "
    if header.account is not None:
        sql += " `account`= '%s' ," % header.account
    if header.password is not None:
        sql += " `password`= '%s' ," % header.password
    if header.cookie is not None:
        sql += " `cookie`= '%s' ," % header.cookie
    if header.referer is not None:
        sql += " `referer`= '%s' ," % header.referer
    if header.user_agent is not None:
        sql += " `user-agent`= '%s' ," % header.user_agent
    if header.status is not None:
        sql += " `status`= %d ," % header.status
    sql = sql[:len(sql) - 1]

    if header.id is not None:
        sql += " where id = %d" % header.id
    elif header.account is not None:
        sql += " where account = '%s'" % header.account
    else:
        return False, " PRIMARY KEY NOT NUll"
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        cursor.close()
        conn.rollback()
        logUtils.logger.error("updateHeaders exception {}", e)
    else:
        logUtils.logger.info("updateHeaders SUCCESS ")
        conn.commit()
        cursor.close()
    finally:
        conn.close()
    return True, "SUCCESS"


def insetHeaders(header):
    sql = "insert into headers(`cookie`,`referer`,`user-agent`,`account`,`password`,`status`) VALUES('%s','%s','%s','%s','%s',%d) "
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        e_sql = sql % (
            header.cookie, header.referer, header.user_agent, header.account, header.password, header.status)
        cursor.execute(e_sql)
    except Exception as e:
        conn.rollback()
        cursor.close()
        logUtils.logger.error("insetHeaders exception {}", e)
        return False, "ERROR"
    else:
        logUtils.logger.info("insetHeaders SUCCESS")
        cursor.close()
        conn.commit()
    finally:
        conn.close()
    return True, "SUCCESS"

def updateHeaderStatus(status,account):
    conn = POOL.connection()
    try:
        sql = "update headers set status = %d where account= '%s'"
        cursor = conn.cursor()
        cursor.execute(sql%(status,account))
        cursor.close()
        conn.commit()
    except Exception as e:
        logUtils.logger.error(u"线程检测出现异常", e, exc_info=True, stack_info=True)
        conn.rollback()
    finally:
        conn.close()



def getHeadersByStatus(status):
    sql = "select select id,cookie,referer,`user-agent`,account,password,status,fail_times  from headers where status = %d " % status
    if headerLock.acquire():
        try:
            conn.ping(True)
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            description = cursor.description
            columns = []
            headers = []
            for i in range(len(description)):
                columns.append(description[i][0])  # 获取字段名，咦列表形式保存
            for i in range(len(result)):
                head = {}
                # 取出每一行 和 列名组成map
                row = list(result[i])
                for j in range(len(columns)):
                    head[columns[j]] = row[j]
                headers.append(head)
        except:
            cursor.close()
            conn.commit()
        else:
            cursor.close()
            conn.commit()
        finally:
            headerLock.release()
    return headers

def getOneHeadersByStatus(status):
    sql = "select id,cookie,referer,`user-agent`,account,password,status,fail_times from headers where status = %d order by update_time ASC limit 1" % status
    conn = POOL.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        description = cursor.description
        columns = []
        headers = []
        for i in range(len(description)):
            columns.append(description[i][0])  # 获取字段名，咦列表形式保存
        for i in range(len(result)):
            head = {}
            # 取出每一行 和 列名组成map
            row = list(result[i])
            for j in range(len(columns)):
                head[columns[j]] = row[j]
            headers.append(head)
        return headers
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()


def getAllHeaders():
    sql = "select id,cookie,referer,`user-agent`,account,password from headers "
    conn = POOL.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        description = cursor.description
        columns = []
        headers = []
        for i in range(len(description)):
            columns.append(description[i][0])  # 获取字段名，咦列表形式保存
        for i in range(len(result)):
            head = {}
            # 取出每一行 和 列名组成map
            row = list(result[i])
            for j in range(len(columns)):
                head[columns[j]] = row[j]
            headers.append(head)
        return headers
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
def getRandItemUrl():
    sql = "select item_url from item_url order by rand() LIMIT 1 "
    conn = POOL.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        description = cursor.description
        columns = []
        urls = []
        for i in range(len(description)):
            columns.append(description[i][0])  # 获取字段名，咦列表形式保存
        for i in range(len(result)):
            head = {}
            # 取出每一行 和 列名组成map
            row = list(result[i])
            for j in range(len(columns)):
                head[columns[j]] = row[j]
            urls.append(head)
        return urls
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
def getRandDisturbUrl():
    sql = "select * from disturb_url order by rand() LIMIT 1 "
    conn = POOL.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        description = cursor.description
        columns = []
        urls = []
        for i in range(len(description)):
            columns.append(description[i][0])  # 获取字段名，咦列表形式保存
        for i in range(len(result)):
            url = {}
            # 取出每一行 和 列名组成map
            row = list(result[i])
            for j in range(len(columns)):
                url[columns[j]] = row[j]
            urls.append(url)
        return urls
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()

def getFailTimes(account):
    sql = "select fail_times from headers where account='%s' "
    conn = POOL.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql%account)
        result = cursor.fetchall()
        description = cursor.description
        columns = []
        fail_times = []
        for i in range(len(description)):
            columns.append(description[i][0])  # 获取字段名，咦列表形式保存
        for i in range(len(result)):
            # 取出每一行 和 列名组成map
            row = list(result[i])
            for j in range(len(columns)):
                fail_times.append(row[j])
        return fail_times
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()



def updateFailTimes(failTimes,account):
    if failTimes is not None:
        sql = "update headers set fail_times = %d  where account='%s' "%(int(failTimes),str(account))
    else:
        sql = "update headers set fail_times = fail_times+1  where account='%s' "%(str(account))
    conn = POOL.connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    except Exception as e:
        conn.rollback()
        conn.close()
        raise  Exception("更新失败次数发生异常")
    finally:
        conn.close()


