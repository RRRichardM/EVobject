"""
Author: RichardM
Date: 2023-12-06 19:55:46
LastEditors: RichardM
LastEditTime: 2024-01-03 17:35:05
Description: 

Copyright (c) 2024 by RichardM, All Rights Reserved. 
"""
# This is a project for Electric Vehicle
import numpy as np
import mysort


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
        # self.tasks=[(remain_power,deadline,changer,cost),...]
        self.tasks = []
        # self.tasks = sorted(self.tasks, key=mysort.EDF)
        self.time_caculate = int_infotmation["time_caculate"]
        self.total_earn = 0

    def add_task(self, new_tasks):
        for task in new_tasks:
            # add cost
            task[3] = self.EVS_price * task[0]
            for i in range(self.num_of_charger):
                if self.occupy_state_charger[-1][i] == 0:
                    self.occupy_state_charger[-1][i] = 1
                    # set the task's charger
                    task[2] = i
                    self.charger_remain -= 1
                    break
        self.tasks = self.tasks.append(new_tasks)

    def renew_state(self):
        self.price = self.price.append(self.pop(0))
        self.occupy_state_charger.append(self.occupy_state_charger[-1])
        reward = 0
        # renew tasks
        for task in self.tasks:
            # task=(remain_power,deadline,changer,cost)
            task[1] -= 1
            if task[1] == 0:
                self.occupy_state_charger[-1][task[2]] = 0
                self.charger_remain += 1
                reward += task[3]
                self.total_earn += reward
                self.tasks.remove(task)
        return reward

    def caculate(self):
        # sort the tasks by LLF_LD
        self.tasks = sorted(self.tasks, key=mysort.LLF_LD)
        # self.tasks = sorted(self.tasks, key=mysort.EDF)

        self.power = [0 for _ in range(self.time_caculate)]
        self.power_remain = [self.power_limit for _ in range(self.time_caculate)]
        # start caculate
        fake_price = self.price.copy()
        for task in self.tasks:
            # task=(remain_power,deadline,changer,cost)
            (
                remain_power,
                deadline,
                changer,
                cost,
            ) = task
            selected_periods = sorted(range(deadline), key=lambda i: fake_price[i])[
                :remain_power
            ]
            for index in selected_periods:
                # deal limit power
                if self.power_remain[index] == 0:
                    task[1] += 1
                    task[3] -= self.max_price * 3
                else:
                    self.power[index] += 1
                    self.power_remain[index] -= 1
                    if self.power_remain[index] == 0:
                        fake_price[index] = self.max_price * 3
                    if index == 0:
                        task[0] -= 1
                        task[3] -= self.price[0]
