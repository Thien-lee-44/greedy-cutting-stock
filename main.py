from CuttingStockEnv import CuttingStockEnv
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2210xxx.policy2210xxx import Policy2210xxx
import numpy as np
from copy import deepcopy
# Create the environment
# env = gym.make(
#     "gym_cutting_stock/CuttingStock-v0",
#    render_mode="human",  # Comment this line to disable rendering
# )
env =CuttingStockEnv(render_mode="human")
NUM_EPISODES = 10

if __name__ == "__main__":
    # Reset the environment

    
    ep = 0
    while ep<NUM_EPISODES:
        observation, info = env.reset(seed=42)
        cpyobs=deepcopy(observation)
        cpyinf=deepcopy(info)
        st_policy= Policy2210xxx()
        print("EP:",ep)
        while True:
            action = st_policy.get_action(observation, info)
            observation, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                print("greedy1",info)
                break
        env._set_obs(cpyobs["stocks"],cpyobs["products"])
        obervation=cpyobs
        info= cpyinf
        gd_policy = GreedyPolicy()
        while True:
            action = gd_policy.get_action(observation, info)
            observation, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                print("greedy2",info)
                ep+=1
                break

    # Reset the environment

    # Test GreedyPolicy
   

    # Test RandomPolicy
    
    # Uncomment the following code to test your policy
    # # Reset the environment
    # observation, info = env.reset(seed=42)
    # print(info)

    # policy2210xxx = Policy2210xxx()
    # for _ in range(200):
    #     action = policy2210xxx.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)
    #     print(info)

    #     if terminated or truncated:
    #         observation, info = env.reset()

env.close()
