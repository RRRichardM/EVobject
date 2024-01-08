import gymnasium as gym
from gymnasium import spaces
import numpy as np
from queue import Queue
from typing import Optional, Tuple, Union
import random
from EVSystem import EVSystem


class MyEnvironment(gym.Env):
    def __init__(self, render_mode: Optional[str] = None):
        super(MyEnvironment, self).__init__()
        self.max_episode_steps: int = 50

        # 定义观测空间
        self.observation_space = spaces.Box(low=0, high=1, dtype=np.float32, shape=(2,))

        # 定义动作空间
        self.action_space = spaces.Discrete(10)

        # 记录当前回合的步数
        self.current_step = 0

        self.state = np.random.rand()

        # 记录当前回合的奖励 是一个队列
        self.action = None
        self.reward = Queue()
        self.EVSysten = EVSystem()

    def step(self, action):
        # 在这里实现环境的状态转移逻辑
        # 根据动作更新环境状态
        self.action = action

        location, _ = self.state
        location = location + action / 10 + (2 * random.random() - 1) * 0.2 - 0.3
        reward = -1
        # 计算奖励s
        # 假设奖励在三个回合后才能体
        self.reward.put(reward)
        self.current_step += 1
        truncated = self.current_step >= self.max_episode_steps
        if (location - 5) ** 2 < 1:
            truncated = True
        self.state = (location, 0)
        return (
            np.array(self.state, dtype=np.float32),
            self.reward.get(),
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
        np.random.seed(seed)
        self.current_step = 0
        self.state = (0, 0)
        self.steps_beyond_terminated = None

        for _ in range(3):
            self.reward.put(-1)
        return np.array(self.state, dtype=np.float32), {}

    def render(self, mode="human"):
        # 在控制台上显示当前状态
        print("Current state:", self.state)
        print("action", self.action)

        # 返回初始观测
        return self.state

    def close(self):
        return super().close()


if __name__ == "__main__":
    env = MyEnvironment()
