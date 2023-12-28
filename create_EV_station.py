"""
Author: RichardM
Date: 2023-12-07 21:18:49
LastEditors: RichardM
LastEditTime: 2023-12-11 16:58:36
Description: 

Copyright (c) 2023 by ${XJTU}, All Rights Reserved. 
"""
import random
import numpy as np


def creat_ev_station():
    # 创建地图概率矩阵
    map_matrix = np.array(
        [
            [2, 1, 1, 1, 1],
            [1, 1, 1, 2, 1],
            [1, 2, 1, 1, 1],
            [1, 2, 2, 2, 1],
            [1, 2, 1, 1, 1],
        ]
    )
    map_matrix = map_matrix / np.sum(map_matrix)
    # 创建充电站位置矩阵
    charging_stations = np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0],
        ]
    )
    # 选择一个随机点
    selected_point = np.random.choice(25, p=map_matrix.flatten())

    # 计算选定点与所有充电站的距离
    distances = np.sqrt(
        np.sum(
            (np.argwhere(charging_stations) - np.unravel_index(selected_point, (5, 5)))
            ** 2,
            axis=1,
        )
    )

    # 找到最近的3个充电站的索引
    nearest_indices = np.argsort(distances)[:3]

    # 获取对应的充电站位置
    nearest_charging_stations = np.argwhere(charging_stations)[nearest_indices]
    return nearest_indices + 1


if __name__ == "__main__":
    creat_ev_station()
