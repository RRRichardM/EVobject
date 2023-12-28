"""
Author: RichardM
Date: 2023-12-11 19:02:51
LastEditors: RichardM
LastEditTime: 2023-12-11 19:23:36
Description: 

Copyright (c) 2023 by ${XJTU}, All Rights Reserved. 
"""
import random
import numpy as np


def create_charge_demand(durable_time):
    probability = np.array(range(0, min(5, durable_time)), dtype=np.float32) + 5
    probability = probability / np.sum(probability)

    charge_demand = np.random.choice(
        range(1, min(6, durable_time + 1)), p=probability.flatten()
    )
    return charge_demand


if __name__ == "__main__":
    create_charge_demand(3)
