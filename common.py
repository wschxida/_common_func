#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : common.py
# @Author: Cedar
# @Date  : 2020/6/9
# @Desc  :

import time
import json
import hashlib
from requests.compat import urljoin
import pymysql
import tldextract
import datetime
import re


def current_time():
    """
    获取当前时间
    :return: 返回格式化后的时间数据
    """
    print("[*] 正在获取当前时间")
    cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    date = datetime.datetime.strptime(cur_time, '%Y-%m-%d %H:%M:%S')
    print("[+] 获取完成")
    return date


def filter_punctuation(input_str):
    """
    过滤标点符号
    :param input_str:
    :return:
    """
    re_punctuation = re.compile("[`~!@#$^&*()=|｜{}':;',\\[\\].《》<>/?~！@#￥……&*（）——|{}【】‘；：”“'\"。，、？%+_]")
    result = re_punctuation.sub('', input_str)
    result = result.strip()
    return result


def match_url(input_str):
    """
    匹配url，规范输出
    :param input_str:
    :return:
    """
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')    # 匹配模式
    url = re.findall(pattern, input_str)
    try:
        result = url[0]
    except Exception as e:
        result = ''
    return result


def get_token(md5str):
    # md5str = "abc"
    # 生成一个md5对象
    m1 = hashlib.md5()
    # 使用md5对象里的update方法md5转换
    m1.update(md5str.encode("utf-16LE"))
    token = m1.hexdigest()
    return token


def query_mysql(config_params, query_sql):
    """
    执行SQL
    :param config_params:
    :param query_sql:
    :return:
    """
    # 连接mysql
    config = {
        'host': config_params["host"],
        'port': config_params["port"],
        'user': config_params["user"],
        'passwd': config_params["passwd"],
        'db': config_params["db"],
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    results = None
    try:
        conn = pymysql.connect(**config)
        conn.autocommit(1)
        # 使用cursor()方法获取操作游标
        cur = conn.cursor()
        cur.execute(query_sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        conn.close()  # 关闭连接
    except Exception as e:
        pass

    return results


def get_domain_code(url):
    domain_code = ''
    domain_info = tldextract.extract(url)
    # print(domain_info)
    if domain_info.domain:
        if is_ip(domain_info.domain):
            domain_code = domain_info.domain
        elif domain_info.suffix:
            domain_code = f"{domain_info.domain}.{domain_info.suffix}"
            if domain_code.find('%') > -1:
                domain_code = ''
    return domain_code.strip('.')


def is_ip(_str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(_str):
        return True
    else:
        return False


if __name__ == '__main__':
    aa = 'http://www.news.fa-today.com/Article/binfen/Index.html'
    bb = get_domain_code(aa)
    print(bb)
