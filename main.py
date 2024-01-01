# This is a project for Electric Vehicle
import numpy as np
import mysort


class EVstation(object):
    def __init__(self, int_infotmation):
        self.name = int_infotmation["name"]
        self.price = int_infotmation["price"]
        self.power_limit = int_infotmation["power_limit"]
        # self.chargerpower_limit = int_infotmation["chargerpower_limit"]
        # self.num_of_charger = int_infotmation["num_of_charger"]
        # self.tasks=[(remain_power,deadline),...]
        self.tasks = int_infotmation["tasks"]
        self.time_caculate = int_infotmation["time_caculate"]
        self.action = self.caculate()

    def caculate(self):
        # sort the tasks by LLF_LD
        self.tasks = sorted(self.tasks, key=mysort.LLF_LD)
        # self.tasks = sorted(self.tasks, key=mysort.EDF)
        self.power = [0 for _ in range(self.time_caculate)]
        self.power_remain = [self.power_limit for _ in range(self.time_caculate)]

        # start caculate
        for task in self.tasks:
            remain_power, deadline = task
