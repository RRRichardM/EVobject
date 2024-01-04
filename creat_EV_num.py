import csv
import os
import random
import numpy as np
import matplotlib.pyplot as plt


def creat_num(days):
    # 定义三个峰的参数
    mean1 = 8  # 第一个峰的位置
    amplitude1 = 50  # 第一个峰的峰高
    std1 = 1.5  # 第一个峰的标准差

    mean2 = 13  # 第二个峰的位置
    amplitude2 = 25  # 第二个峰的峰高
    std2 = 1  # 第二个峰的标准差

    mean3 = 18  # 第三个峰的位置
    amplitude3 = 50  # 第三个峰的峰高
    std3 = 2  # 第三个峰的标准差

    # 生成x轴的数值范围,起始值、终止值和数列中的元素数量
    x = np.linspace(0, 24, 24 * 60)

    # 根据正态分布公式计算三个峰的曲线
    y1 = amplitude1 * np.exp(-0.5 * ((x - mean1) / std1) ** 2)
    y2 = amplitude2 * np.exp(-0.5 * ((x - mean2) / std2) ** 2)
    y3 = amplitude3 * np.exp(-0.5 * ((x - mean3) / std3) ** 2)
    # 将三个峰的曲线叠加在一起
    y = y1 + y2 + y3
    y_all = np.tile(y, days)
    y_all = y_all + np.random.normal(0, 5, len(y_all))
    # 获取每个小时的索引
    hour_indices = np.arange(0, 24 * 60 * days, 60)
    # 获取每个小时对应的 y 值
    # 正整数
    hourly_y = y_all[hour_indices]
    hourly_y = np.clip(hourly_y, 0, None)
    hourly_y = np.round(hourly_y).astype(int)
    return hourly_y.tolist()


if __name__ == "__main__":
    hourly_y = creat_num(5)
    # 绘制曲线
    plt.plot(hourly_y[:24], "ro")
    plt.xlabel("time")
    plt.ylabel("vale")
    plt.title("EVs num in 24 hours")
    plt.show()
