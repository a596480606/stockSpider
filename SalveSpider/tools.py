#encoding=utf8
"""
# -*- coding: utf-8 -*-
"""
import pymysql
import requests

class Mysql:

    def __init__(self, MysqlHost, MysqlPort, MysqlUser, MysqlPassword, MysqlDB):
        self.conn = pymysql.connect(host=MysqlHost, port=MysqlPort, user=MysqlUser, password=MysqlPassword, db="")
        if self.conn:
            print("连接成功")
        self.cursor = self.conn.cursor()

        # 当 MysqlDB 不存在时创建它，并切换到 MysqlDB 数据库
        self.cursor.execute("Create Database If Not Exists {} Character Set UTF8;".format(MysqlDB))
        self.cursor.execute("use {};".format(MysqlDB))

    def execute(self,sql):
        self.cursor.execute(sql)


def get_stock_price(code):
    """
    通过股票代码，模拟请求从东方财富网获取交易日数据
    :param code: 股票代码
    :return: 股票名称、300个交易日的日K数据
    """
    url = "http://22.push2his.eastmoney.com/api/qt/stock/kline/get"
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive', 'Cookie': 'qgqp_b_id=ea1333abfc79cea5c265f9d77159fdf7; HAList=a-sh-600410-%u534E%u80DC%u5929%u6210; em_hq_fls=js; st_si=94908642787912; emshistory=%5B%22600410%22%5D; st_asi=delete; st_pvi=06885083096584; st_sp=2020-03-05%2010%3A46%3A18; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=4; st_psi=20200313135500750-113200301201-9886509617', 'Host': '22.push2his.eastmoney.com', 'Referer': 'http://quote.eastmoney.com/sh600410.html', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

    # 可以通过 lmt 设置返回交易日信息的数量，这里返回最近 300 个交易日
    params = {
        'cb': 'jQuery112408624872486898423_1584078899740',
        'secid': '{}.{}'.format("0" if code[0] in ("0","3") else "1", code),
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        'fields1': 'f1,f2,f3,f4,f5',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58',
        'klt': '101',
        'fqt': '0',
        'end': '20500101',
        'lmt': '300',
        '_': '1584078899802'
    }
    # 对返回的数据进行处理
    resp = requests.get(url=url, headers=headers, params=params)
    data = eval(resp.text[resp.text.index("{"):-2].replace("false","False").replace("null", "'null'"))["data"]
    name = data["name"]
    price_data = data["klines"]
    return name, price_data

