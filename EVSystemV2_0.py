from EVstationV2_0 import EVstation
from EV_station_data import generate_int_information
import os
import pandas as pd
import logging
from datetime import datetime


class EVSystem(object):
    def __init__(self, EVS_num=5):
        self.EVS_num = EVS_num
        self.EVstations = self.create_EVstation(self.EVS_num)
        self.time_caculate = self.EVstations[0].time_caculate
        self.power_limit = self.EVstations[0].power_limit
        self.filename = "dataset_one_30.csv"
        self.filepath = os.path.join("data", self.filename)
        self.EV_requests = pd.read_csv(self.filepath)
        self.data_start_index = 0
        self.run_time = 0
        self.total_run_time = 24
        self.current_request = []
        self.total_earn = 0
        self.task_num = 0
        # # log当前时间
        # logging.basicConfig(
        #     filename=f"EVSystem_{datetime.now().strftime('%Y%m%d%H%M')}.log",
        #     level=logging.DEBUG,
        # )

    def create_EVstation(self, EVS_num):
        int_infotmations = generate_int_information(EVS_num)
        EV_stations = []
        for int_infotmation in int_infotmations:
            EV_stations.append(EVstation(int_infotmation))
        return EV_stations

    def creat_task(self):
        if self.EV_requests.loc[self.data_start_index, "Time"] != self.run_time % 24:
            return None, True
        EV_request = [
            self.EV_requests.loc[self.data_start_index, "Charge_demand"],
            self.EV_requests.loc[self.data_start_index, "Durable_time"],
            None,
            None,
        ]
        self.data_start_index += 1
        if self.EV_requests.loc[self.data_start_index, "Time"] != self.run_time % 24:
            renew_flag = True
        else:
            renew_flag = False
        return EV_request, renew_flag

    def renew_state(self):
        EVSystem.total_earn = 0
        for EVstation in self.EVstations:
            EVstation.step()
            EVSystem.total_earn += EVstation.true_total_earn


if __name__ == "__main__":
    EVSystem = EVSystem()  # Instantiate the EVSystem class
    i = 0
    while EVSystem.run_time < EVSystem.total_run_time:
        reward = 0
        task, renew_flag = EVSystem.creat_task()
        if task:
            reward = EVSystem.EVstations[i].add_task(task)
        if renew_flag:
            for EVstation in EVSystem.EVstations:
                EVSystem.renew_state()
            EVSystem.run_time += 1

        i += 1
        i = i % EVSystem.EVS_num
        print("run_time:", EVSystem.run_time)
        print("total_earn:", EVSystem.total_earn)
        print("reward:", reward)
