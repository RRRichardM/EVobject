'''
Author: RichardM
Date: 2024-01-01 20:01:24
LastEditors: RichardM
LastEditTime: 2024-01-01 20:02:54
Description: 

Copyright (c) 2024 by ${XJTU}, All Rights Reserved. 
'''
def minimize_cost(t, n, cost):
    # 创建一个二维数组dp来保存最小成本
    dp = [[float('inf')] * (n + 1) for _ in range(t + 1)]
    dp[0][0] = 0

    for hour in range(1, t + 1):
        for ones in range(n + 1):
            # 尝试将当前小时设置为0
            dp[hour][ones] = min(dp[hour][ones], dp[hour - 1][ones])

            # 尝试将当前小时设置为1，并更新成本
            if ones > 0:
                dp[hour][ones] = min(dp[hour][ones], dp[hour - 1][ones - 1] + cost[hour - 1])

    # 找到总成本最小的动作组合
    actions = []
    hour = t
    ones = n
    while hour > 0:
        # 当前小时的动作为0，表示没有选择1
        if dp[hour][ones] == dp[hour - 1][ones]:
            actions.append(0)
        # 当前小时的动作为1，表示选择了1
        else:
            actions.append(1)
            ones -= 1
        hour -= 1

    # 将动作组合反转，使得顺序与时间对应
    actions.reverse()

    return actions

if __name__ == '__main__':
    # 测试用例
    t = 5
    n = 3
    cost = [2, 1, 3, 2, 4]
    actions = minimize_cost(t, n, cost)
    print(actions)