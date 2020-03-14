"""
# -*- coding: utf-8 -*-
"""
import re
import time
import requests


def get_sz_stocks():
    """
    获取深交所所有股票代码，及名称
    :return:
    """
    start = time.time()
    PageMaxNum = 200                        # 获取页数
    stock_dicts = {}
    reg = re.compile("<u>([\S\s]*?)</u>")   # 提取股票名称的正则
    # source_url = "http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110x&TABKEY=tab1&PAGENO={}&random=0.5803427274752198"
    source_url = "http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO={}&random=0.6069632679760002"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "www.szse.cn",
        "Referer": "http://www.szse.cn/market/companys/company/index.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        "X-Request-Type": "ajax",
        "X-Requested-With": "XMLHttpRequest"
    }

    for_flag = False

    for i in range(1, PageMaxNum):

        for t in range(3):
            try :
                resp = requests.get(url=source_url.format(i), headers=headers)
                data = eval(resp.text.replace("false","False").replace("null", "'null'"))
                # 当页数大于 111 且  data 为空，说明没有数据了
                if not data[0]["data"] and i > 111:
                    for_flag = True
                    break

                for d in data[0]["data"]:
                    stock_code = d["zqdm"]
                    # stock_name = reg.findall(d["gsjc"])[0]
                    stock_name = d["agjc"]
                    stock_dicts[stock_name] = stock_code

            except Exception as e:
                if t != 3:
                    print(f"获取深交所第{i}页数据失败，将于5秒后重试！")
                    time.sleep(5)
                else:
                    print(f"获取深交所第{i}页数据失败！")

            else:
                print(f"获取深交所第{i}页数据成功！")
                break
        if for_flag:
            break

    end = time.time()
    print("用时：",end-start)
    return stock_dicts


def get_sh_stocks():
    """
    获取上交所所有股票代码，及名称
    :return:
    """
    stock_dicts = {}
    url = "http://query.sse.com.cn/security/stock/getStockListData2.do"
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive', 'Host': 'query.sse.com.cn', 'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    # 通过修改 pageHelp.pageSize 参数可以自定义返回多少条数据
    params = {
        'jsonCallBack': 'jsonpCallback47257',
        'isPagination': 'true',
        'stockCode': '',
        'csrcCode': '',
        'areaName': '',
        'stockType': '1',
        'pageHelp.cacheSize': '1',
        'pageHelp.beginPage': '3',
        'pageHelp.pageSize': '1000',
        'pageHelp.pageNo': '2',
        'pageHelp.endPage': '21',
        '_': '1584065645969'
    }

    for i in range(1,6):
        params["pageHelp.beginPage"] = str(i)
        resp = requests.get(url=url,headers=headers,params=params)
        resp = resp.text[resp.text.index("{"):-1]
        data = eval(resp.replace("false","False").replace("null", "'null'"))
        if not data['pageHelp']['data']:
            break
        for d in data['pageHelp']['data']:
            stock_dicts[d["COMPANY_ABBR"]] = d["COMPANY_CODE"]
        print(f"获取上交所第{i}页数据成功！")
    return stock_dicts


def get_kcb_stocks():
    stock_dicts = {}
    url = "http://query.sse.com.cn/security/stock/getStockListData.do"
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive', 'Host': 'query.sse.com.cn', 'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    params = {
        'jsonCallBack': 'jsonpCallback47257',
        'isPagination': 'true',
        'stockCode': '',
        'csrcCode': '',
        'areaName': '',
        'stockType': '8',
        'pageHelp.cacheSize': '1',
        'pageHelp.beginPage': '3',
        'pageHelp.pageSize': '1000',
        'pageHelp.pageNo': '2',
        'pageHelp.endPage': '21',
        '_': '1584065645969'
    }

    for i in range(1,6):
        params["pageHelp.beginPage"] = str(i)
        resp = requests.get(url=url,headers=headers,params=params)
        resp = resp.text[resp.text.index("{"):-1]
        data = eval(resp.replace("false","False").replace("null", "'null'"))
        if not data['pageHelp']['data']:
            break
        for d in data['pageHelp']['data']:
            stock_dicts[d["COMPANY_ABBR"]] = d["COMPANY_CODE"]
        print(f"获取上交所科创板第{i}页数据成功！")

    return stock_dicts





