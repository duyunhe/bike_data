# coding=utf-8
from csv_conn.csv_data import get_bike_area
import matplotlib.pyplot as plt


def draw(a, name, c):
    x, y = zip(*a)
    plt.plot(x, y)
    plt.text(c[0], c[1], name)


area_list, name_list, c_list = get_bike_area('./data/tb_area_max.txt')
for area, name, c in zip(area_list, name_list, c_list):
    draw(area, name, c)
plt.show()
