# encoding: utf-8
from numpy import long
from rediscluster import RedisCluster
import pickle
import random
import time

# 根据产生的随机数，来判断该走哪一个代理
LOADBALANCE_THRESHOLD = 100

# 从redis获取ip时不获取5s后即将失效的ip
QINGGUO_PROXY_THRE_SHOLD = 5

RETRY_DECREASING_STEP = 10

QINGGUO_PROXY_PREFIX = "QG_"

AVAILABLE_PROXY_NUM = "AVAILABLE_PROXY_NUM"

# redis中缓存代理云代理的key对应的前缀
DAILIYUN_PROXY_PREFIX = "DLY_"

PROXY_DETAIL = 'proxy_detail'
PROXY_SUPPLIER = 'proxy_supplier'
REDIS_PROXY_KEY = 'redis_proxy_key'

# redis中缓存的代理云的个数对应的key
AVALIABLE_DAILIYUN_PROXY_NUM = "AVALIABLE_DAILIYUN_PROXY_NUM"

# redis集群
startup_nodes = [
    {"host": "10.7.8.120", "port": 8385},
    {"host": "10.7.9.120", "port": 8386},
    {"host": "10.7.9.120", "port": 8385},
    {"host": "10.7.8.139", "port": 8386},
    {"host": "10.7.8.139", "port": 8385},
    {"host": "10.7.8.120", "port": 8386}
]


class redis_cluster_pool(object):
    __pool = None

    def __init__(self):
        __pool = redis_cluster_pool.get_conn()

    @staticmethod
    def get_conn():
        if redis_cluster_pool.__pool is None:
            try:
                redis_cluster_pool.__pool = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, password='BX6AREoe')
                #print('redis cluster connection info %s ' % redis_cluster_pool.__pool.info())
            except Exception as e:
                print ('redis connect exception', e)

        return redis_cluster_pool.__pool

    @staticmethod
    def direct_conn():
        redis_cluster_pool.__pool = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)


def build_query_proxy_redis_key(build_key_prefix, num):
    return build_key_prefix + str(num)


def build_proxy(proxy_detail, proxy_supplier):
    if proxy_detail and proxy_detail != '' and proxy_supplier and proxy_supplier != '' \
            and isinstance(proxy_detail, dict):
        return dict(proxy_detail=proxy_detail['redis_proxy_value'], proxy_supplier=proxy_supplier,
                    redis_proxy_key=proxy_detail['redis_proxy_key'])
    return None


def get_current_time():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - long(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp


def get_current_time_stamp():
    return int(round(time.time()))


def get_one_proxy_from_redis(build_key_prefix, available_proxy_num):
    redis_cluster = redis_cluster_pool.get_conn()
    get_proxy_num = redis_cluster.get(available_proxy_num)
    if not get_proxy_num:
        return None
    valiable_num = int(get_proxy_num)
    while valiable_num > 0:
        try:
            rand_num_try = random.randint(1, valiable_num)
            # redis缓存代理时，key的形式是DLY_211，首字母_数字，DLY_:表示代理是代理云的，QG_表示代理使用的是青果的
            try_query_key = build_query_proxy_redis_key(build_key_prefix, rand_num_try)
            # 根据构建的key获取代理
            try_get_proxy = redis_cluster.get(try_query_key)
            if try_get_proxy:
                format_try_proxy = pickle.loads(try_get_proxy.encode())
                if isinstance(format_try_proxy, dict):
                    expire_time = format_try_proxy.get('time', 0)
                    dead_line = int(expire_time)
                    if dead_line - get_current_time_stamp() > QINGGUO_PROXY_THRE_SHOLD:
                        return dict(redis_proxy_value=format_try_proxy, redis_proxy_key=try_query_key)
        except Exception as e:
            print('%s , get one proxy exception , exception: %s ' % (get_current_time(), e))
        # 如果获取不到代理，降低范围，while循环重新获取
        valiable_num = valiable_num - RETRY_DECREASING_STEP

    return None


# 从redis中获取青果代理，目前青果 & 代理云两种代理，比例分配为各50%
def get_proxy_from_redis():
    # 从1~100中随机取出一个数，如果大于50，走青果代理，小于50走代理云代理，可以通过该值调整代理分配的权重
    random_num = random.randint(1, LOADBALANCE_THRESHOLD)
    # 目前使用青果 & 代理云两种代理，比例分配为各50%
    if random_num > 50:
        one_proxy = get_one_proxy_from_redis(QINGGUO_PROXY_PREFIX, AVAILABLE_PROXY_NUM)
        proxy_supplier = QINGGUO_PROXY_PREFIX
    else:
        one_proxy = get_one_proxy_from_redis(DAILIYUN_PROXY_PREFIX, AVALIABLE_DAILIYUN_PROXY_NUM)
        proxy_supplier = DAILIYUN_PROXY_PREFIX

    if not one_proxy:
        #print( "time: %s , not get %s proxy from redis , try qingguo" % (get_current_time(), proxy_supplier))
        # 备用逻辑，如果没有获取到代理，则再走一次青果代理
        one_proxy = get_one_proxy_from_redis(QINGGUO_PROXY_PREFIX, AVAILABLE_PROXY_NUM)
        proxy_supplier = QINGGUO_PROXY_PREFIX

    if isinstance(one_proxy, dict):
        #print("time:%s , proxy from %s redis:%s" % (get_current_time(), proxy_supplier, one_proxy))
        return build_proxy(one_proxy, proxy_supplier)
    return ''


if __name__ == '__main__':
    get_redis_result = get_proxy_from_redis()
    print('从redis中获取到的代理信息：%s' % get_redis_result)  # redis中缓存的直接结果
    qingguo_proxy = get_redis_result[PROXY_DETAIL]
    print('代理信息：%s' % qingguo_proxy)
    if isinstance(qingguo_proxy, dict):
        print('代理IP：%s' % qingguo_proxy['ip'])
    else:
        print('代理IP：%s' % qingguo_proxy)
    proxy_supplier = get_redis_result[PROXY_SUPPLIER]
    print('代理所属供应商：%s' % proxy_supplier)  # DLY_:表示代理是代理云的，QG_表示代理使用的是青果的
    redis_proxy_key = get_redis_result[REDIS_PROXY_KEY]
    print('redis存储代理key的形式：%s' % redis_proxy_key)
