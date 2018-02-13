# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import time
import urllib2
import json
from pre.geo import xy2bl


class Info(object):
    def __init__(self, n, addr, cnt, x, y):
        self.n, self.addr, self.cnt = n, addr, cnt
        self.x, self.y = x, y

    def __lt__(self, other):
        return self.cnt > other.cnt


def point_to_addr_new(point):
    ulr = "http://restapi.amap.com/v3/geocode/regeo?location={0},{1}" \
          "&key=0a54a59bdc431189d9405b3f2937921a&radius=100&extensions=all".format(point[0], point[1])
    for fails in range(0, 4):
        try:
            if fails >= 3:
                print 'timeout'
                return None
            temp = urllib2.urlopen(ulr, timeout=10)
            t = temp.read()
        except Exception, e:
                print e
                print '网络连接出现问题, 正在尝试再次请求:'.decode('utf8'), fails
        else:
            try:
                temp = json.loads(t)
                list0 = temp['regeocode']['formatted_address']
                return list0
            except KeyError:
                print 'error'
                return None


def get_data():
    xy_list = []
    f = open("./data/bike_normal.txt", 'r')
    for line in f.readlines():
        items = line.split(',')
        x, y = float(items[0]), float(items[1])
        xy_list.append((x, y))
    return xy_list


def xy_dict():
    xy_list = get_data()
    X = np.array(xy_list)
    tb = time.time()
    # y_pred = DBSCAN(eps=120, min_samples=300).fit_predict(X)
    db = DBSCAN(eps=60, min_samples=1000, n_jobs=-1).fit(X)
    eb = time.time()
    print 'dbscan time {0}'.format(eb - tb)
    labels = db.labels_
    x_dict = {}
    y_dict = {}
    label = set(labels)
    for t in label:
        x_dict[t] = []
        y_dict[t] = []
    for i in range(0, len(labels)):
        x_dict[labels[i]].append(X[:, 0][i])
        y_dict[labels[i]].append(X[:, 1][i])
    return x_dict, y_dict


x_dict, y_dict = xy_dict()
print len(x_dict)
color = ['ro', 'bo', 'go', 'co', 'mo', 'yo', 'ko', 'rs', 'bs', 'gs',
         'ms', 'y*', 'cs', 'ks', 'r^', 'g^', 'k^', 'c^', 'm^', 'b^',
         'yd', 'r*', 'b*', 'g*', 'm*', 'c*', 'k*', 'y^', 'b+', 'g+',
         'c+', 'm+', 'k+', 'rp', 'bp', 'gp', 'cp', 'yp', 'mp', 'kp',
         'rd', 'r+', 'gd', 'cd', 'ys', 'kd', 'md', 'bd', 'rx', 'bx',
         'gx', 'cx', 'mx', 'yx', 'kx', 'r>', 'b>', 'g>', 'y>', 'm>',
         'y+']

max_size = 0
spot_info = []
for n in x_dict:
    if n == -1:
        plt.plot(x_dict[n], y_dict[n], color[-1], alpha=0.2)
    else:
        plt.plot(x_dict[n], y_dict[n], color[n % 30], alpha=0.2)
        max_size = max(len(x_dict[n]), max_size)
        vec = np.array([x_dict[n], y_dict[n]])
        ave = np.mean(vec, axis=1)
        x, y = ave[0:2]
        lat, lng = xy2bl(x, y)
        addr = point_to_addr_new([lng, lat])
        plt.text(x, y, str(n))
        # print n, addr, len(x_dict[n])
        info = Info(n, addr, len(x_dict[n]), lng, lat)
        spot_info.append(info)

spot_info = sorted(spot_info)
for info in spot_info:
    print info.n, info.addr, info.cnt, "{0},{1}".format(info.x, info.y)

print max_size
plt.show()
