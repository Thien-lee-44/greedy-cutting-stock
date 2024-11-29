from CuttingStockEnv import CuttingStockEnv
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2210xxx.policy2210xxx import *
from copy import deepcopy
from time import time,sleep
# Create the environment
# env = gym.make(
#     "gym_cutting_stock/CuttingStock-v0",
#    render_mode="human",  # Comment this line to disable rendering
# )
env =CuttingStockEnv(
     render_mode="human"
                     )
NUM_EPISODES = 1

if __name__ == "__main__":
    # Reset the environment
    ep = 0
    
    cpolicy= CPolicy()
    ffpolicy = FFPolicy()
    bfpolicy =BFPolicy()
    while ep<NUM_EPISODES:
        observation, info = env.reset(seed=42)
        cpyobs=deepcopy(observation)
        cpyinf=deepcopy(info)
        print("EP:",ep)
        start_time = time()
        while True:
            action = cpolicy.get_action(observation, info)
            observation, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                end_time = time()
                print("combine",info,"time:",round(end_time-start_time,2),"second")
                sleep(2)
                break
        env._set_obs(cpyobs["stocks"],cpyobs["products"])
        observation=cpyobs
        info= cpyinf
        cpyobs=deepcopy(observation)
        cpyinf=deepcopy(info)
        start_time = time()
        while True:
            action = bfpolicy.get_action(observation, info)
            observation, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                end_time = time()
                print("best fit",info,"time:",round(end_time-start_time,2),"second")
                break
        env._set_obs(cpyobs["stocks"],cpyobs["products"])
        observation=cpyobs
        info= cpyinf
        cpyobs=deepcopy(observation)
        cpyinf=deepcopy(info)
        start_time = time()
        while True:
            action = ffpolicy.get_action(observation, info)
            observation, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                end_time = time()
                print("First fit",info,"time:",round(end_time-start_time,2),"second")
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
