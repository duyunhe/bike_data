# -*- coding: utf-8 -*-
# @Time    : 2018/3/2 15:31
# @Author  : 
# @简介    : 
# @File    : everyday.py

from csv_conn import csv_data
import time


def main():
    filename = './data/tb_bike_gps_1711.csv'
    date_format = '%Y-%m-%d %H:%M:%S'
    bt = time.clock()
    csv_data.get_bike_last_data(filename, date_format)
    et = time.clock()
    print et - bt


main()
