# coding=utf-8
__author__ = 'cd'
from datetime import datetime
from geo import bl2xy


def process_data():
    f = open("../data/tb_bike_gps_1802.csv", 'r')
    fp1 = open('../data/bike_08.txt', 'w')
    fp2 = open('../data/bike_18.txt', 'w')
    cnt = 0
    for line in f.readlines():
        if cnt == 0:
            cnt = 1
            continue
        items = line.split(',')
        lng, lat = float(items[4].strip('"')), float(items[5].strip('"'))
        if lng > 121 or lng < 119 or lat > 31 or lat < 29:
            continue
        x, y = bl2xy(lat, lng)
        state = int(items[7].strip('"'))
        stime = items[3].strip('"')
        dtime = datetime.strptime(stime, '%Y/%m/%d %H:%M:%S')
        if state == 0:
            new_str = "{0},{1},{2}\n".format(x, y, stime)
            if 6 <= dtime.hour < 9 and dtime.day <= 5:
                fp1.write(new_str)
            elif 16 <= dtime.hour < 19 and dtime.day <= 5:
                fp2.write(new_str)
        cnt += 1
    fp1.close()
    fp2.close()


def process_txt():
    f = open('../data/bike.txt', 'r')
    fw = open('../data/bike_normal.txt', 'w')
    for line in f.readlines():
        items = line.split(',')
        lng, lat = float(items[0]), float(items[1])
        if lng > 121 or lng < 119 or lat > 31 or lat < 29:
            continue
        stime = items[2].strip('\n')
        dtime = datetime.strptime(stime, '%Y/%m/%d %H:%M:%S')
        if 6 <= dtime.hour <= 24:
            fw.write(line)
    fw.close()

# process_data()
process_txt()