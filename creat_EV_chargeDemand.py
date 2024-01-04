import random
import numpy as np


def create_charge_demand(durable_time):
    probability = np.arange(min(8, durable_time)) + 1
    if durable_time > 8:
        probability[-1] = probability[-1] + (durable_time - 8) * 4
    probability = probability / np.sum(probability)

    charge_demand = np.random.choice(
        range(1, min(9, durable_time + 1)), p=probability.flatten()
    )
    return charge_demand


if __name__ == "__main__":
    for i in range(10):
        print(create_charge_demand(8))
