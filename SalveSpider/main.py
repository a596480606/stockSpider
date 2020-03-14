"""
# -*- coding: utf-8 -*-
"""
import time
import redis
from tools import Mysql, get_stock_price
from settings import RedisHost, RedisPort, RedisPassword, RedisDB
from settings import MysqlHost, MysqlPort, MysqlUser, MysqlPassword, MysqlDB


start = time.time()

# 建表和插入数据的sql语句
create_table_sql = """Create Table If Not Exists a{}(date varchar(10),code char(6),name varchar(16),open varchar(10),close varchar(10),high varchar(10),low varchar(10),amount varchar(10),vol varchar(20),num int(10) auto_increment,primary key(num)) default character set=utf8;"""
insert_sql_1 = """insert into a"""
insert_sql_2 = """(date, code, name, open, close, high, low, amount, vol) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

# 连接 redis 和 mysql 数据库
R = redis.Redis(host=RedisHost, port=RedisPort, password=RedisPassword, db=RedisDB)
DB = Mysql(MysqlHost, MysqlPort, MysqlUser, MysqlPassword, MysqlDB)


# 循环从 stock 队列获取股票代码
while True:
    # 当队列为空终止循环
    if R.llen("stock") == 0:
        print(f"redis 列表为空，终止循环！")
        break

    # 从队列获取一个股票代码
    code = R.lpop("stock")
    code = str(code,"utf8")

    new_sql = insert_sql_1 + code + insert_sql_2        # 组装插入数据的 sql 语句
    sql_data = []                                       # 存放sql数据的字典

    # 在 mysql 中为每只股票创建一个表
    cs = create_table_sql.format(code)
    DB.execute(cs)

    # 调用函数从东方财富网获取数据，并插入数据库
    name, price_data = get_stock_price(code)
    for d in price_data:
        k = d.split(",")
        date = k[0]         # 交易日日期
        open = k[1]         # 开盘价
        close = k[2]        # 收盘价
        high = k[3]         # 最高价
        low = k[4]          # 最低价
        amount = k[5]       # 成交量
        vol = k[6]          # 成交额
        sql_data.append((date,code,name,open,close,high,low,amount,vol))        # 组装数据

    # 调用 executemany() 插入数据，可以极大地提高插入速度
    DB.cursor.executemany(new_sql,sql_data)
    DB.conn.commit()
    print(f"{code} 下载成功！")

end = time.time()
print(end - start)



