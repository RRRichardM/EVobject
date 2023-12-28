"""
Author: RichardM
Date: 2023-12-11 18:24:27
LastEditors: RichardM
LastEditTime: 2023-12-11 18:34:13
Description: 

Copyright (c) 2023 by ${XJTU}, All Rights Reserved. 
"""
import random
import numpy as np


def create_durable_time(timenow):
    timeprosibility = np.array(
        [2, 2, 3, 4, 5, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        dtype=np.float32,
    )
    for i in range(timeprosibility.shape[0]):
        if (timenow + i) % 24 >= 22 or (timenow + i) % 24 <= 6:
            timeprosibility[i] = timeprosibility[i] * 0.5
    timeprosibility = timeprosibility / np.sum(timeprosibility)
    durable_time = np.random.choice(range(1, 25), p=timeprosibility.flatten())
    return durable_time


if __name__ == "__main__":
    create_durable_time(1)
