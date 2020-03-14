"""
# -*- coding: utf-8 -*-
"""
import time
import redis
from tools import get_sz_stocks, get_sh_stocks, get_kcb_stocks
from settings import RedisHost, RedisPort, RedisPassword, RedisDB


start = time.time()

# 连接 redis 数据库
R = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPassword, db=RedisDB)

# 存放股票代码的字典
stock_dicts = {}

# 从深交所、上交所获取全部 A 股代码
sz_stocks = get_sz_stocks()
sh_stocks = get_sh_stocks()
kcb_stocks = get_kcb_stocks()

# 更新字典
stock_dicts.update(sz_stocks)
stock_dicts.update(sh_stocks)
stock_dicts.update(kcb_stocks)

# 把 股票代码 放入redis队列
for key in stock_dicts:
    R.rpush("stock", stock_dicts[key])

end = time.time()

print("用时:",end - start)


