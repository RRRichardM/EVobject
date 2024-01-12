from ray.rllib.algorithms import SAC
from env_EV_rllib import MyEnvironment as MyEnv
from ray.tune.registry import register_env
from gymnasium.wrappers import FlattenObservation


def env_creator(env_config):  # 此处的 env_config对应 我们在建立trainer时传入的dict env_config
    MyEnv = FlattenObservation(MyEnv)  # 传入的参数
    return MyEnv(...)  # return an env instance


register_env("my_env", env_creator)  # 此处传入了 环境的名称 | 环境的实例调用函数
algo = SAC(env="my_env", config={})  # 传入 env的__init__中
