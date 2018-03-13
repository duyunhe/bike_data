# -*- coding: utf-8 -*-
# @Time    : 2018/3/8 10:29
# @Author  : Du
# @简介    : 蜂窝
# @File    : hive.py

import shapefile
import matplotlib.pyplot as plt
import math
import numpy as np
from pre import geo
import time

benchmark = np.zeros((900, 900))
# 每一行的基准


class HiveGrid:
    def __init__(self, row, col, center):
        self.center = center
        self.row, self.col = row, col


def ch2int(ch):
    return ord(ch) - ord('A')


def str2int(name):
    ans = 0
    if len(name) == 1:
        return ord(name) - ord('A')
    elif len(name) == 2:
        return (ch2int(name[0]) + 1) * 26 + ch2int(name[1])
    elif len(name) == 3:
        return (ch2int(name[0]) + 1) * 26 * 26 + (ch2int(name[1]) + 1) * 26 + ch2int(name[2])
    return ans


def draw_hive(grid_list):
    x, y = map(list, zip(*grid_list))
    plt.plot(x, y)
    for g in grid_list:
        print g[0], g[1]
    # plt.text(grid[0][0], grid[0][1], name)


def get_col(row, x):
    lo, hi = 0, 899
    while lo < hi - 1:
        m = (lo + hi) / 2
        t = benchmark[row][m]
        if t > x:
            hi = m
        elif t < x:
            lo = m
        else:
            return m
    if x < benchmark[row][hi]:
        m = lo
    return m


def get_line(point, center, hive):
    defy = center[1]
    x, y = point[0], point[1]
    dy = 187.637024826 * 2
    dx = 325.425575026
    dr = int((y - defy) / dy)
    row = 725 - dr

    col = get_col(row, x)
    # print col

    if col & 1:
        try:
            pts = [hive[row][col - 1], hive[row][col], hive[row - 1][col]]
        except KeyError:
            return [-1, -1]
    else:
        try:
            pts = [hive[row][col], hive[row][col + 1], hive[row - 1][col]]
        except KeyError:
            return [-1, -1]
    min_dist = 1e10
    sel_coord = []
    for pt in pts:
        vec = np.array(point)
        dist = np.linalg.norm(vec - pt.center)
        if dist < min_dist:
            min_dist = dist
            sel_coord = [pt.row, pt.col]
    # print sel_coord
    return sel_coord


def draw_item(hive):
    d = {}
    c = {}
    for i, v in hive.items():
        for j in v.keys():
            row = i * 2 - (j & 1)
            col = j
            try:
                c[col].append([hive[i][j].center[0], (i, j)])
                d[row].append([hive[i][j].center[1], (i, j)])
            except KeyError:
                d[row] = [[hive[i][j].center[1], (i, j)]]
                c[col] = [[hive[i][j].center[0], (i, j)]]

    levs = []
    vets = []
    for row in d.keys():
        x, _ = zip(*d[row])
        hi = np.mean(np.array(x))
        levs.append(hi)

    for col in c.keys():
        x, _ = zip(*c[col])
        hi = np.mean(np.array(x))
        vets.append(hi)
    # levs.sort()
    itv = []
    for i in range(len(vets) - 1):
        itv.append(vets[i + 1] - vets[i])
    hi = np.mean(np.array(itv))
    print hi
    x = [i for i in range(len(vets) - 1)]
    plt.scatter(x, itv)
    plt.show()


def read_grid():
    grid = {}
    fp = open(".\hive\grid.txt")

    for line in fp.readlines():
        items = line.strip('\n').split(',')
        irow, icol = map(int, items[0:2])
        g_list = []
        for i in range(7):
            g_list.append([float(items[i * 2 + 2]), float(items[i * 2 + 3])])
        try:
            grid[irow][icol] = g_list
        except KeyError:
            grid[irow] = {icol: g_list}
    return grid


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
    return map_index, map_index[725][286].center


def main():
    map_index, coord_center = read_hive()
    # sf = shapefile.Reader(".\hive\hive.shp")
    # rec = sf.records()
    #
    # map_index = {}
    # coord_center = [1e20, 1e20]
    # sel_hg = None
    # fp = open(".\hive\hive.txt", 'w')
    #
    # for i in range(len(rec)):
    #     name = rec[i][0]
    #     items = name.split('-')
    #     col, row = items[0], items[1]
    #     irow = int(row)
    #     icol = str2int(col)
    #     sp = sf.shape(i)
    #     pts = sp.points
    #     str_pts = []
    #     # fp.write("{0},{1},".format(irow, icol))
    #     for j in range(len(pts)):
    #         str_pts.append("{0},{1}".format(pts[j][0], pts[j][1]))
    #         pts[j] = list(geo.bl2xy(pts[j][1], pts[j][0]))
    #     str_line = ','.join(str_pts)
    #     # fp.write(str_line + '\n')
    #     cx, cy = (pts[0][0] + pts[3][0]) / 2, (pts[0][1] + pts[3][1]) / 2
    #     center = np.array([cx, cy])
    #     b, l = geo.xy2bl(cx, cy)
    #     hg = HiveGrid(irow, icol, center, np.array([b, l]))
    #     fp.write("{0},{1},{2},{3}\n".format(irow, icol, center[0], center[1], b, l))
    #     try:
    #         map_index[irow][icol] = hg
    #     except KeyError:
    #         map_index[irow] = {icol: hg}
    #     if coord_center[1] > center[1]:
    #         coord_center = center
    #         sel_hg = hg
    #
    # print sel_hg.row, sel_hg.col
    # fp.close()
    def_center = coord_center.copy()
    cnt, sel = 0, 0
    for i in map_index.keys():
        if cnt < len(map_index[i]):
            cnt, sel = len(map_index[i]), i

    sintha = 0.0057
    costha = math.sqrt(1 - sintha ** 2)
    trans_tha = [[costha, sintha], [-sintha, costha]]
    trans_atha = [[costha, -sintha], [sintha, costha]]
    # draw_item(map_index)

    for i in map_index.keys():
        _min, _max = 1e10, 0
        for j in map_index[i].keys():
            hg = map_index[i][j]
            hg.center -= def_center
            hg.center = np.dot(hg.center, trans_tha)
            benchmark[i][j] = hg.center[0]
            if j < _min:
                _min = j
            if j > _max:
                _max = j
        for j in range(0, _min):
            benchmark[i][j] = -1e10
        for j in range(_max + 1, 900):
            benchmark[i][j] = 1e10

    # draw_item(map_index)
    # get_line(map_index[465][456].center, coord_center, 725, 286, map_index)

    px, py = map_index[465][456].center[0:2]
    print px, py
    pt = np.dot(map_index[465][456].center, trans_atha)
    lat, lng = geo.xy2bl(pt[1], pt[0])
    # pt = np.dot(np.array([px, py]), trans_tha)
    # lat, lng = geo.xy2bl(px, py)
    row, col = get_line(np.array([px, py]), coord_center, map_index)
    print row, col
    grid = read_grid()
    draw_hive(grid[row][col])
    print lng, lat
    plt.plot(lng, lat)
    plt.show()


main()
