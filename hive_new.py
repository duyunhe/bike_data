# -*- coding: utf-8 -*-
# @Time    : 2018/3/13 8:35
# @Author  : 
# @简介    : 
# @File    : hive_new.py

import shapefile
import numpy as np
import time

unitx = 0.00336868231321
unity = 0.00338976483195
benchmark = np.ones((900, 900)) * 180
# 每一列的y基准


class HiveGrid:
    def __init__(self, row, col, center):
        self.center = center
        self.row, self.col = row, col


def ch2int(ch):
    return ord(ch) - ord('A')


def get_row(col, y):
    lo, hi = 0, 899
    m = (lo + hi) / 2
    while lo < hi - 1:
        m = (lo + hi) / 2
        t = benchmark[m][col]
        if t < y:
            hi = m
        elif t > y:
            lo = m
        else:
            return m
    if y > benchmark[hi][col]:
        m = lo
    return m


def str2int(name):
    ans = 0
    if len(name) == 1:
        return ord(name) - ord('A')
    elif len(name) == 2:
        return (ch2int(name[0]) + 1) * 26 + ch2int(name[1])
    elif len(name) == 3:
        return (ch2int(name[0]) + 1) * 26 * 26 + (ch2int(name[1]) + 1) * 26 + ch2int(name[2])
    return ans


def read_shape():
    sf = shapefile.Reader(".\hive\hive.shp")
    rec = sf.records()

    fp = open(".\hive\hive.txt", 'w')
    for i in range(len(rec)):
        name = rec[i][0]
        items = name.split('-')
        col, row = items[0], items[1]
        irow = int(row)
        icol = str2int(col)
        sp = sf.shape(i)
        pts = sp.points
        cx, cy = (pts[0][0] + pts[3][0]) / 2, (pts[0][1] + pts[3][1]) / 2
        center = np.array([cx, cy])
        hg = HiveGrid(irow, icol, center)
        fp.write("{0},{1},{2},{3}\n".format(irow, icol, center[0], center[1]))
    fp.close()


def read_hive():
    map_index = {}
    fp = open(".\hive\hive.txt")
    for line in fp.readlines():
        items = line.strip('\n').split(',')
        irow, icol = map(int, items[0:2])
        cx, cy = map(float, items[2:4])
        center = np.array([cx, cy])
        hg = HiveGrid(irow, icol, center)
        try:
            map_index[irow][icol] = hg
        except KeyError:
            map_index[irow] = {icol: hg}
        benchmark[irow][icol] = hg.center[1]
    for j in range(900):
        maxi = 0
        for i in range(900):
            if benchmark[i][j] < 180:
                maxi = i
        for i in range(maxi + 1, 900):
            benchmark[i][j] = 0
    return map_index, map_index[725][286].center


def get_pos(point, center):
    dpt = point - center
    dx, dy = dpt[0:2]
    col = 286 + int(dx / unitx)
    row = get_row(col, point[1])
    # print row, col
    return row, col


def main():
    hive_index, center = read_hive()
    bt = time.clock()
    for i in hive_index.keys():
        for _, v in hive_index[i].items():
            get_pos(v.center, center)
    et = time.clock()
    print et - bt

main()
