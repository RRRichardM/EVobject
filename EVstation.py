"""
Author: RichardM
Date: 2023-12-06 19:55:46
LastEditors: RichardM
LastEditTime: 2024-01-04 19:21:14
Description: 

Copyright (c) 2024 by RichardM, All Rights Reserved. 
"""
# This is a project for Electric Vehicle
import numpy as np
import mysort
from EV_station_data import generate_int_information


class EVstation(object):
    def __init__(self, int_infotmation):
        self.name = int_infotmation["name"]
        self.location = int_infotmation["location"]
        self.price = int_infotmation["price"]
        self.max_price = max(self.price)
        self.EVS_price = 2 * self.max_price
        self.power_limit = int_infotmation["power_limit"]
        self.power_log = []
        # self.chargerpower_limit = int_infotmation["chargerpower_limit"]
        self.num_of_charger = int_infotmation["num_of_charger"]
        self.charger_remain = self.num_of_charger
        self.occupy_state_charger = [[0 for _ in range(self.num_of_charger)]]
        # self.tasks=[[remain_power,deadline,changer,cost],...]
        self.tasks = []
        self.opt_state = int_infotmation["opt_state"]

        self.time_caculate = int_infotmation["time_caculate"]
        self.total_earn = 0

    def add_task(self, new_tasks):
        if not new_tasks:
            return
        for task in new_tasks:
            # add cost
            task[3] = self.EVS_price * task[0]
            for i in range(self.num_of_charger):
                if self.occupy_state_charger[-1][i] == 0:
                    self.occupy_state_charger[-1][i] = 1
                    # set the task's charger
                    task[2] = i
                    self.charger_remain -= 1
                    self.tasks.append(task)
                    break
                if i == self.num_of_charger - 1:
                    print("error: no enough charger")

    def renew_state(self):
        self.price.append(self.price.pop(0))
        self.occupy_state_charger.append(self.occupy_state_charger[-1])
        reward = 0
        task_to_remove = []
        # renew tasks
        for task in self.tasks:
            task[1] -= 1
            # task=[remain_power,deadline,changer,cost]
            if task[1] == 0:
                if task[0] != 0:
                    task[3] -= self.EVS_price
                    task[1] += 1
                else:
                    self.occupy_state_charger[-1][task[2]] = 0
                    self.charger_remain += 1
                    reward += task[3]
                    task_to_remove.append(task)
                continue
        self.total_earn += reward
        for task in task_to_remove:
            self.tasks.remove(task)
        return reward

    def caculate(self):
        if not self.tasks:
            return
        # sort the tasks by LLF_LD
        if self.opt_state == 0:
            self.power = [0 for _ in range(self.time_caculate)]
            self.power_remain = [self.power_limit for _ in range(self.time_caculate)]
            # start caculate
            for task in self.tasks:
                if task[0] == 0:
                    continue
                if self.power_remain[0] == 0:
                    break
                else:
                    task[0] -= 1
                    task[3] -= self.price[0]
                    self.power[0] += 1
                    self.power_remain[0] -= 1

        elif self.opt_state == 1 or self.opt_state == 2:
            if self.opt_state == 1:
                # sort the tasks by EDF
                self.tasks = sorted(self.tasks, key=mysort.EDF)
            if self.opt_state == 2:
                self.tasks = sorted(self.tasks, key=mysort.LLF_LD)
            self.power = [0 for _ in range(self.time_caculate)]
            self.power_remain = [self.power_limit for _ in range(self.time_caculate)]
            # start caculate
            fake_price = self.price.copy()
            for task in self.tasks:
                # task=[remain_power,deadline,changer,cost]
                (
                    remain_power,
                    deadline,
                    changer,
                    cost,
                ) = task
                if remain_power == 0:
                    continue
                selected_periods = sorted(range(deadline), key=lambda i: fake_price[i])[
                    :remain_power
                ]
                for index in selected_periods:
                    # deal limit power
                    if self.power_remain[index] == 0:
                        continue
                    else:
                        self.power[index] += 1
                        self.power_remain[index] -= 1
                        if self.power_remain[index] == 0:
                            fake_price[index] = self.max_price * 3
                        if index == 0:
                            task[0] -= 1
                            task[3] -= self.price[0]
