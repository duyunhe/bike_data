# -*- coding: utf-8 -*-
# @Time    : 2018/3/5 11:18
# @Author  : C.D
# @简介    : 
# @File    : get_mysql.py

import MySQLdb
from DBUtils.PooledDB import PooledDB
from datetime import datetime, timedelta

sql_settings = {'mysql': {'host': '60.191.16.73', 'port': 6052, 'user': 'bike',
                          'passwd': 'bike', 'db': 'bike'}}
pool = PooledDB(creator=MySQLdb,
                mincached=1, maxcached=20,
                use_unicode=True, charset='utf8',
                **sql_settings['mysql'])


def save(day):
    dt = datetime(2017, 12, day)
    tmr = dt + timedelta(days=1)
    stime0 = dt.strftime('%Y-%m-%d')
    fp = open('data/1712/{0}.csv'.format(stime0), 'w')
    sql = "select * from tb_bike_gps_1712 where positiontime >= '{0}' and positiontime < '{1}'".format(
        stime0, tmr.strftime('%Y/%m/%d')
    )
    conn = pool.connection()
    cur = conn.cursor()
    cur.execute(sql)
    for item in cur.fetchall():
        fp.write('{0},{1},{2},{3},{4}\n'.format(item[0], item[1], item[2], item[3], item[4]))
    fp.close()


for i in range(4, 32):
    save(i)

