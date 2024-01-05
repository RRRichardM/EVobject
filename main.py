"""
Author: RichardM
Date: 2024-01-03 20:22:47
LastEditors: RichardM
LastEditTime: 2024-01-04 20:11:55
Description: 

Copyright (c) 2024 by RichardM, All Rights Reserved. 
"""
from EVstation import EVstation
from EV_station_data import generate_int_information
import os
import pandas as pd
import logging


def create_EVstation(EVS_num):
    int_infotmations = generate_int_information(EVS_num)
    EV_stations = []
    for int_infotmation in int_infotmations:
        EV_stations.append(EVstation(int_infotmation))
    return EV_stations


if __name__ == "__main__":
    logging.basicConfig(filename=f"test1.log", level=logging.DEBUG)
    EVstations = create_EVstation(1)
    filename = "dataset_one_30.csv"
    filepath = os.path.join("data", filename)
    EV_requests = pd.read_csv(filepath)

    data_start_index = 0
    run_time = 0
    total_run_time = 24 * 30
    while run_time < total_run_time:
        print("run_time:", run_time)
        EV_request = []
        current_time = run_time % 24
        while True:
            if EV_requests.loc[data_start_index, "Time"] != current_time:
                break
            else:
                # task=[remain_power,deadline,changer,cost]
                EV_request.append(
                    [
                        EV_requests.loc[data_start_index, "Charge_demand"],
                        EV_requests.loc[data_start_index, "Durable_time"],
                        None,
                        None,
                    ]
                )
                data_start_index += 1
        # lack of assigning task to EVstation
        for EVstation in EVstations:
            EVstation.add_task(EV_request)
            EVstation.caculate()
            reward = EVstation.renew_state()
            logging.info(
                f"run_time:{run_time},reward:{reward},total_earn:{EVstation.total_earn}"
            )
            logging.info(f"EVstation.tasks:{EVstation.tasks}")
            print("reward:", reward)
            print("total_earn:", EVstation.total_earn)

        run_time += 1
