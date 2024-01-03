"""
Author: RichardM
Date: 2024-01-01 20:37:57
LastEditors: RichardM
LastEditTime: 2024-01-02 20:24:21
Description: 

Copyright (c) 2024 by RichardM, All Rights Reserved. 
"""


def LLF_LD(tasks):
   # self.tasks=[(remain_power,deadline,changer,cost),...]
    # sort the tasks by LLF_LD
    remain_power, deadline,changer,cost = tasks
    slack = deadline - remain_power
    return (slack, -deadline)


def EDF(tasks):
    # self.tasks=[(remain_power,deadline,changer,cost),...]
    # sort the tasks by EDF
    remain_power, deadline,changer,cost = tasks
    return deadline


if __name__ == "__main__":
    tasks = [(3, 10,None,1), (4, 8,1,1), (2, 6,2,3), (2, 12,3,4), (1, 5,1,4)]
    sorted_tasks = sorted(tasks, key=LLF_LD)
    print("LLF_LD: ", sorted_tasks)
    sorted_tasks = sorted(tasks, key=EDF)
    print("EDF: ", sorted_tasks)
