# -*- coding: utf-8 -*-
# @Time    : 2018/3/13 8:35
# @Author  : 
# @简介    : 
# @File    : hive_new.py

import numpy as np
import time
from pre import geo
import matplotlib.pyplot as plt

unitx = 0.00336868231321
unity = 0.00338976483195
benchmark_y = np.ones((900, 900)) * 180         # 每一列的y基准
benchmark_x = [0] * 900                         # 每一列的x值
hive_index = None


class HiveGrid:
    def __init__(self, row, col, center, pts):
        self.center = center
        self.row, self.col = row, col
        self.pts = pts


def ch2int(ch):
    return ord(ch) - ord('A')


def get_col(x):
    lo, hi = 0, 899
    m = (lo + hi) / 2
    while lo < hi - 1:
        m = (lo + hi) / 2
        t = benchmark_x[m]
        if t < x:
            lo = m
        elif t > x:
            hi = m
        else:
            return m
    if x > benchmark_x[lo]:
        m = lo
    return m


def get_row(col, y):
    lo, hi = 0, 899
    m = (lo + hi) / 2
    while lo < hi - 1:
        m = (lo + hi) / 2
        t = benchmark_y[m][col]
        if t < y:
            hi = m
        elif t > y:
            lo = m
        else:
            return m
    if y < benchmark_y[lo][col]:
        m = hi
    return m


def draw_hive(hive_grid):
    pts = hive_grid.pts
    x, y = zip(*pts)
    plt.plot(x, y)
    str_line = "{0},{1}".format(hive_grid.row, hive_grid.col)
    plt.text(hive_grid.center[0], hive_grid.center[1], str_line)


def draw_around(row, col, hive):
    for i in range(-2, 3):
        for j in range(-2, 3):
            r, c = row + i, col + j
            try:
                draw_hive(hive[r][c])
            except KeyError:
                continue
    plt.show()


def str2int(name):
    ans = 0
    if len(name) == 1:
        return ord(name) - ord('A')
    elif len(name) == 2:
        return (ch2int(name[0]) + 1) * 26 + ch2int(name[1])
    elif len(name) == 3:
        return (ch2int(name[0]) + 1) * 26 * 26 + (ch2int(name[1]) + 1) * 26 + ch2int(name[2])
    return ans


def read_hive():
    map_index = {}
    fp = open(".\hive\hive.txt")
    for line in fp.readlines():
        items = line.strip('\n').split(',')
        irow, icol = map(int, items[0:2])
        cx, cy = map(float, items[2:4])
        pts = []
        for i in range(4, 11):
            xy = map(float, items[i].split(':'))
            pts.append(xy)
        center = np.array([cx, cy])
        hg = HiveGrid(irow, icol, center, pts)
        try:
            map_index[irow][icol] = hg
        except KeyError:
            map_index[irow] = {icol: hg}
        benchmark_y[irow][icol] = hg.center[1]
        benchmark_x[icol] = hg.center[0]

    # 生成有序x，y基准值
    max_mark = 0
    for j in range(900):
        if benchmark_x[j] > 0:
            max_mark = benchmark_x[j]
        else:
            benchmark_x[j] = max_mark
    for j in range(900):
        min_mark = 180
        for i in range(900):
            if benchmark_y[i][j] < 180:
                min_mark = benchmark_y[i][j]
            else:
                benchmark_y[i][j] = min_mark
    return map_index


def get_pos(point, hive):
    col = get_col(point[0])
    row = get_row(col, point[1])
    # print row, col
    pts = []
    try:
        pts.append(hive[row][col])
        pts.append(hive[row - 1][col])
        if col & 1:
            pts.append(hive[row - 1][col + 1])
        else:
            pts.append(hive[row][col + 1])
    except KeyError:
        pass
    min_dist = 1e10
    for pt in pts:
        dist = geo.haversine(point[0], point[1], pt.center[0], pt.center[1])
        if dist < min_dist:
            min_dist = dist
            row, col = pt.row, pt.col
    return row, col


def draw_list(lst):
    x = [i for i in range(len(lst))]
    plt.scatter(x, lst)
    plt.show()


def main(x, y):
    global hive_index
    pt = np.array([x, y])
    return get_pos(pt, hive_index)


def init():
    bt = time.clock()
    global hive_index
    hive_index = read_hive()
    et = time.clock()
    print 'hive init', et - bt


def test():
    init()
    cnt, tot = 0, 0
    for i in hive_index.keys():
        for j, v in hive_index[i].items():
            r, c = main(v.center[0] - 0.0001, v.center[1] - 0.0001)
            tot += 1
            if i != r or c != j:
                cnt += 1
    print cnt, tot


test()
