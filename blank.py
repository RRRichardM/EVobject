price = [10, 5, 8, 3, 1]  # 价格列表
deadline = 4  # 截止日期
remain_power = 2  # 剩余电力

selected_periods = sorted(range(deadline), key=lambda i: price[i])[:remain_power]

print(selected_periods)
