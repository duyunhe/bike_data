# -*- coding: utf-8 -*-
# @Time    : 2018/3/2 15:31
# @Author  : 
# @简介    : 
# @File    : everyday.py

from csv_conn import csv_data
import time


def main():
    filename = './data/test.csv'
    bt = time.clock()
    csv_data.get_bike_last_data(filename)
    et = time.clock()
    print et - bt


main()
