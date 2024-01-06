from EVstation import EVstation
from EV_station_data import generate_int_information
import os
import pandas as pd
import logging
from datetime import datetime


class EVSystem(object):
    def __init__(self, EVS_num=5):
        self.EVS_num = EVS_num
        self.EVstations = self.create_EVstation(self.EVS_num)
        self.filename = "dataset_one_30.csv"
        self.filepath = os.path.join("data", self.filename)
        self.EV_requests = pd.read_csv(self.filepath)
        self.data_start_index = 0
        self.run_time = 0
        self.total_run_time = 24 * 30
        self.current_request = []
        # log当前时间
        logging.basicConfig(
            filename=f"EVSystem_{datetime.now().strftime('%Y%m%d%H%M')}.log",
            level=logging.DEBUG,
        )

    def create_EVstation(EVS_num):
        int_infotmations = generate_int_information(EVS_num)
        EV_stations = []
        for int_infotmation in int_infotmations:
            EV_stations.append(EVstation(int_infotmation))
        return EV_stations

    def creat_request(self):
        if self.current_request != []:
            return self.current_request
        EV_request = []
        current_time = self.run_time % 24
        while True:
            if (
                self.EV_requests.loc[self.data_start_index, "Time"] != current_time
                or self.data_start_index >= self.total_run_time
            ):
                break
            else:
                # task=[remain_power,deadline,changer,cost]
                EV_request.append(
                    [
                        self.EV_requests.loc[self.data_start_index, "Charge_demand"],
                        self.EV_requests.loc[self.data_start_index, "Durable_time"],
                        None,
                        None,
                    ]
                )
                self.data_start_index += 1
        return EV_request

    def step_run(self, action):
        reward = 0
        self.current_request = self.creat_request()
        request = self.current_request[0]
        self.current_request.pop(0)
        refuse_fee = self.EVstations[action].add_task([request])
        if refuse_fee != None:
            reward -= refuse_fee
        #  all request has been assigned to EVstation
        if self.current_request == []:
            for EVstation in self.EVstations:
                EVstation.caculate()
                reward += EVstation.renew_state()
        logging.info(f"run_time:{self.run_time},reward:{reward}")
        return reward
