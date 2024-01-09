import csv
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from create_EV_station import creat_ev_station
from creat_EV_num import creat_num
from create_EV_durableTime import create_durable_time
from creat_EV_chargeDemand import create_charge_demand


def creat_data(days):
    datalist = []
    nums = creat_num(days)
    id = 0
    for time, num in enumerate(nums):
        # 单站测试
        num = round(num / 3)
        for i in range(num):
            timenow = time % 24
            ev_station = creat_ev_station()
            durable_time = create_durable_time(timenow)
            charge_demand = create_charge_demand(durable_time)
            datalist.append([id, timenow, ev_station, durable_time, charge_demand])
            id += 1

    return datalist


def generate_csv_dataset(filename, days):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # 写入 CSV 文件的标题行
        writer.writerow(["ID", "Time", "EV_station", "Durable_time", "Charge_demand"])
        data_lsit = creat_data(days)
        # 生成随机数据并写入 CSV 文件
        for data in data_lsit:
            writer.writerow(data)


if __name__ == "__main__":
    # 确保 "data" 文件夹存在
    if not os.path.exists("data"):
        os.makedirs("data")
        # 拼接完整的文件路径

    # 指定生成的 CSV 文件名和行数
    filename = "dataset_one_30.csv"
    filepath = os.path.join("data", filename)
    days = 30

    # 生成 CSV 数据集
    generate_csv_dataset(filepath, days)

    print(f"{filename} 文件已成功生成。")
