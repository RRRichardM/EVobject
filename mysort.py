"""
Author: RichardM
Date: 2024-01-01 20:37:57
LastEditors: RichardM
LastEditTime: 2024-01-01 20:49:10
Description: 

Copyright (c) 2024 by ${XJTU}, All Rights Reserved. 
"""


def LLF_LD(tasks):
    # tasks=[(remain_power,deadline),...]
    # sort the tasks by LLF_LD
    remain_power, deadline = tasks
    slack = deadline - remain_power
    return (slack, -deadline)


def EDF(tasks):
    # tasks=[(remain_power,deadline),...]
    # sort the tasks by EDF
    remain_power, deadline = tasks
    return deadline


if __name__ == "__main__":
    tasks = [(3, 10), (4, 8), (2, 6), (2, 12), (1, 5)]
    sorted_tasks = sorted(tasks, key=LLF_LD)
    print("LLF_LD: ", sorted_tasks)
    sorted_tasks = sorted(tasks, key=EDF)
    print("EDF: ", sorted_tasks)
