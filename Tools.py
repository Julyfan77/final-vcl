# coding=utf-8
import math


def get_distance(p1, p2):
    """
    计算两点之间距离
    :param p1: 点A
    :param p2: 点B
    :return: 距离
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def get_del(a, b, c, d):
    """
    计算行列式的值
    |a  b|
    |c  d|
    """
    return a * d - b * c


def decompose(p1, p2, p, origin=(0, 0)):
    """
    对向量进行分解
    :param p1: 基底A
    :param p2: 基底B
    :param p: 待分解向量
    :param origin: 原点坐标
    :return: 得到的系数(x, y)
    """
    a1 = p1[0] - origin[0]
    b1 = p1[1] - origin[1]
    a2 = p2[0] - origin[0]
    b2 = p2[1] - origin[1]
    del_d = get_del(a1, a2, b1, b2)
    del_x = get_del(p[0] - origin[0], a2, p[1] - origin[1], b2)
    del_y = get_del(a1, p[0] - origin[0], b1, p[1] - origin[1])
    return float(del_x) / del_d, float(del_y) / del_d
