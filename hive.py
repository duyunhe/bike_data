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


def draw_hive(hive):
    for name, vec in hive.items():
        x, y = map(list, zip(*vec[1]))
        plt.plot(x, y)
        plt.text(vec[0][0], vec[0][1], name)


def draw_item(hive):
    d = {}
    for i, v in hive.items():
        for j in v.keys():
            row = i + (j & 1)
            try:
                d[row].append(hive[i][j].center[1])
            except KeyError:
                d[row] = [hive[i][j].center[1]]

    levs = []
    for row in d.keys():
        hi = np.mean(np.array(d[row]))
        levs.append(hi)
    levs.sort()
    itv = []
    for i in range(len(levs) - 1):
        itv.append(levs[i + 1] - levs[i])
    x = [i for i in range(len(levs) - 1)]
    plt.scatter(x, itv)
    plt.show()


def main():
    sf = shapefile.Reader(".\hive\hive.shp")
    rec = sf.records()

    map_index = {}

    coord_center = None
    for i in range(len(rec)):
        name = rec[i][0]
        items = name.split('-')
        col, row = items[0], items[1]
        irow = int(row)
        icol = str2int(col)
        sp = sf.shape(i)
        pts = sp.points
        for j in range(len(pts)):
            pts[j] = list(geo.bl2xy(pts[j][1], pts[j][0]))
        cx, cy = (pts[0][0] + pts[3][0]) / 2, (pts[0][1] + pts[3][1]) / 2
        center = np.array([cx, cy])
        hg = HiveGrid(irow, icol, center)
        try:
            map_index[irow][icol] = hg
        except KeyError:
            map_index[irow] = {icol: hg}
        coord_center = center

    cnt, sel = 0, 0
    for i in map_index.keys():
        if cnt < len(map_index[i]):
            cnt, sel = len(map_index[i]), i

    sintha = 0.0057
    costha = math.sqrt(1 - sintha ** 2)
    trans_tha = [[costha, sintha], [-sintha, costha]]
    # draw_item(map_index)

    for i in map_index.keys():
        for j in map_index[i].keys():
            hg = map_index[i][j]
            hg.center -= coord_center
            hg.center = np.dot(hg.center, trans_tha)
    draw_item(map_index)

main()


