# -*- coding: utf-8 -*-
# @Time    : 2018/3/2 14:06
# @Author  : C.D.
# @简介    : 读取自行车csv数据公共库
# @File    : csv_data.py
from datetime import datetime


def read_title(line):
    """
    :param line: 读取的头行
    :return: var_name：变量名字符串列表
    """
    temp = line.strip('\n').split(',')
    items = [one.strip('\"') for one in temp]
    return items


def get_data_daily(filename, state='all'):
    """

    :param filename: 文件名
    :param state:  借还车状态: '0'代表借车 '1'代表未借车 默认为'all'代表所有状态
    :return: {data} 按日期为key的每日信息列表
    """
    fp = open(filename, 'r')

    data = {}
    line = fp.readline()
    var = locals()
    var_name = read_title(line)

    for line in fp.readlines():
        temp = line.strip('\n').split(',')
        items = [one.strip('\"') for one in temp]
        for name, item in zip(var_name, items):
            var[name] = item
        if state != 'all' and var['State'] != state:
            continue
        bid = "{0}:{1}".format(var['CompanyId'], var['BicycleNo'])
        str_time = var['PositionTime']
        position_time = datetime.strptime(str_time, '%Y/%m/%d %H:%M:%S')

        day_time = position_time.strftime('%Y/%m/%d')
        try:
            data[day_time].append(items)
        except KeyError:
            data[day_time] = []
            data[day_time].append(items)

    fp.close()
    return data


def get_data_by_bike(filename, date_format):
    fp = open(filename, 'r')

    data = {}
    line = fp.readline()
    var = locals()
    var_name = read_title(line)

    idx = 0
    with open(filename, 'rb') as fp:
        for line in fp:
            if idx == 0:
                idx = 1
                continue
            temp = line.strip('\n').split(',')
            items = [one.strip('\"') for one in temp]
            for name, item in zip(var_name, items):
                var[name] = item
            bid = "{0}:{1}".format(var['CompanyId'], var['BicycleNo'])
            str_time = var['PositionTime']
            position_time = datetime.strptime(str_time, date_format)

            day_time = position_time.strftime('%Y/%m/%d')
            try:
                data[bid].append(items)
            except KeyError:
                data[bid] = []
                data[bid].append(items)
            idx += 1
            if idx % 10000 == 0:
                print idx

    fp.close()
    return data


def get_data_by_day(filename, state='all'):
    fp = open(filename, 'r')

    data = {}
    line = fp.readline()
    var = locals()
    var_name = read_title(line)

    for line in fp.readlines():
        temp = line.strip('\n').split(',')
        items = [one.strip('\"') for one in temp]
        for name, item in zip(var_name, items):
            var[name] = item
        if state != 'all' and var['State'] != state:
            continue
        bid = "{0}:{1}".format(var['CompanyId'], var['BicycleNo'])
        str_time = var['PositionTime']
        position_time = datetime.strptime(str_time, '%Y/%m/%d %H:%M:%S')

        day_time = position_time.strftime('%Y/%m/%d')
        try:
            data[day_time][bid].append(items)
        except KeyError:
            try:
                data[day_time][bid] = []
            except KeyError:
                data[day_time] = {}
                data[day_time][bid] = []
            data[day_time][bid].append(items)

    fp.close()
    return data


def get_bike_last_data_by_day(filename):
    datas = get_data_by_day(filename)
    bike_status_list = {}
    for day in datas:
        bike_status_list[day] = []
        for bike, data_list in datas[day].items():
            bike_status_list[day].append(datas[day][bike][-1])
    return bike_status_list


def get_bike_last_data(filename, date_format):
    datas = get_data_by_bike(filename, date_format)
    bike_status_list = {}
    for bid, data_list in datas.items():
        bike_status_list[bid] = datas[bid][-1]
    return bike_status_list


def get_bike_area(filename):
    fp = open(filename, 'r')
    data_list, name_list, center_list = [], [], []

    for line in fp.readlines():
        temp = line.strip('\n').split('\t')
        items = [one.strip('\"') for one in temp]
        name = items[0]
        name_list.append(name)
        xy = map(float, items[2].split(','))
        center_list.append(xy)

        coord = items[4].split(';')
        xy_list = []
        for co in coord:
            xy = map(float, co.split(','))
            xy_list.append(xy)
        data_list.append(xy_list)
    return data_list, name_list, center_list

