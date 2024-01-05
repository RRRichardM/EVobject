import csv
import os
import random
import numpy as np
import matplotlib.pyplot as plt

EVS_coordinate = [(1, 2), (1, 4), (2, 1), (3, 3), (4, 1)]


def caculate_price():
    electric_prices = [0.55] * 24  # 平段电价为0.55

    # 设置低谷时段电价
    electric_prices[23] = electric_prices[23] * 0.37  # 低谷电价为平段电价下浮63%
    for i in range(0, 6):
        electric_prices[i] = electric_prices[i] * 0.37  # 低谷电价为平段电价下浮63%

    # 设置高峰时段电价
    for i in range(8, 11):
        electric_prices[i] = electric_prices[i] * 1.5  # 高峰电价为平段电价上浮50%

    for i in range(18, 23):
        electric_prices[i] = electric_prices[i] * 1.5  # 高峰电价为平段电价上浮50%

    # 设置尖峰时段电价
    for i in range(19, 21):
        electric_prices[i] = electric_prices[i] * 1.2  # 尖峰电价为高峰电价上浮20%

    # 计算24小时电费
    hourly_costs = [electric_prices[i] for i in range(24)]
    return hourly_costs


def generate_int_information(EVS_num):
    EVS_coordinate = [(1, 2), (1, 4), (2, 1), (3, 3), (4, 1)]
    hourly_costs = caculate_price()
    int_infotmations = []

    for i in range(EVS_num):
        int_infotmation = {}
        int_infotmation["name"] = "EV_station" + str(i)
        int_infotmation["location"] = EVS_coordinate[i]
        int_infotmation["price"] = hourly_costs
        int_infotmation["power_limit"] = 10
        int_infotmation["opt_state"] = 0
        int_infotmation["num_of_charger"] = 20
        int_infotmation["time_caculate"] = 48

        int_infotmations.append(int_infotmation)
    return int_infotmations
