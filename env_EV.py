import gymnasium as gym
from gymnasium import spaces
import numpy as np
from queue import Queue
from typing import Optional, Tuple, Union
import random
from EVSystem import EVSystem
from gymnasium.spaces.utils import flatten_space
from gymnasium.spaces.utils import flatten
from collections import OrderedDict
import logging

# log当前时间
logging.basicConfig(filename="test.log", level=logging.DEBUG)


class MyEnvironment(gym.Env):
    def __init__(self, render_mode: Optional[str] = None):
        super(MyEnvironment, self).__init__()
        self.max_episode_steps: int = 24
        self.EVSystem = EVSystem(5)
        self.total_earn = self.EVSystem.total_earn
        self.max_demand_power = 8
        self.reward = 0
        self.EVS_num = self.EVSystem.EVS_num
        self.time_caculate = self.EVSystem.time_caculate
        # 定义观测空间
        # task=[remain_power,deadline,changer,cost]
        self.observation_space = spaces.Dict(
            {
                "stations_remain_charge_state": spaces.MultiBinary(self.EVS_num),
                # "stations_power_remain": spaces.MultiDiscrete(
                #     [self.EVSystem.power_limit + 1 for _ in range(self.time_caculate)]
                #     * self.EVS_num
                # ),
                # "stask": spaces.MultiDiscrete(
                #     [self.max_demand_power + 1, self.time_caculate + 1]
                # ),
            }
        )
        # self.observation_space = flatten_space(self.observation_space)

        # 定义动作空间
        self.action_space = spaces.Discrete(self.EVS_num)

        self.EVSystem = EVSystem()

    def step(self, action):
        # 在这里实现环境的状态转移逻辑

        self.action = action
        reward = self.EVSystem.step_run(action)
        request = self.EVSystem.creat_request()
        if not request:
            task = [0, 0]
        else:
            task = [request[0][0], request[0][1]]

        state = OrderedDict()
        # state["stask"] = np.array(task)
        # state["stations_power_remain"] = np.array(
        #     [EVstation.power_remain for EVstation in self.EVSystem.EVstations]
        # ).flatten()
        state["stations_remain_charge_state"] = np.array(
            [EVstation.remain_charge_state for EVstation in self.EVSystem.EVstations]
        )

        if self.EVSystem.run_time >= self.max_episode_steps:
            truncated = True
        else:
            truncated = False
        self.state = flatten(self.observation_space, state)
        self.reward = reward

        return (
            self.state,
            reward,
            truncated,
            False,
            {},
        )

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        self.EVSystem = EVSystem(5)

        np.random.seed(seed)
        request = self.EVSystem.creat_request()
        if not request:
            task = [0, 0]
        else:
            task = [request[0][0], request[0][1]]

        state = OrderedDict()
        # state["stask"] = np.array(task)
        # state["stations_power_remain"] = np.array(
        #     [EVstation.power_remain for EVstation in self.EVSystem.EVstations]
        # ).flatten()
        state["stations_remain_charge_state"] = np.array(
            [EVstation.remain_charge_state for EVstation in self.EVSystem.EVstations]
        )
        self.state = flatten(self.observation_space, state)
        print("正在重置！")
        return self.state, {}

    def render(self, mode="human"):
        # 在控制台上显示当前状态
        logging.info("Current state: %s", self.state)
        logging.info("Current action: %s", self.action)
        logging.info("running_time %s", self.EVSystem.run_time)
        logging.info("Current reward: %s", self.reward)
        logging.info("Current total_earn: %s", self.EVSystem.total_earn)
        print("Current state:", self.state)
        print("Current action:", self.action)
        print("running_time", self.EVSystem.run_time)
        print("Current reward:", self.reward)
        print("Current total_earn:", self.EVSystem.total_earn)

        # 返回初始观测
        return self.state

    def close(self):
        return super().close()


if __name__ == "__main__":
    env = MyEnvironment()
    print(env.observation_space)
