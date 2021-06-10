from os.path import dirname, join, abspath
import time 
import numpy as np
from enviroment import ReacherEnv
from collections import deque
import torch
from agent import Agent
import matplotlib.pyplot as plt
import torch.optim as optim

EPISODES = 10000
EPISODE_LENGTH = int(50)
SCENE_FILE = join(dirname(abspath(__file__)), 'cenarios/espeleo.ttt')

env = ReacherEnv(SCENE_FILE,False)
agent = Agent(state_size=16, action_size=5, seed=0)
replay_buffer = []
scores = []
mean = []
scores_window = deque(maxlen=100)
eps = 1.0
loss = []
t = 0

best = -9999.0


agent.qnetwork_local.load_state_dict(torch.load('dicionario_pth/checkpoint_espeleo_posvar3.pth'))
b = 0
for i in range(1,20):
    state = env.reset()
    score = 0
    for j in range(200):
        action = agent.act(state)

        done, reward, next_state = env.step(action)
        agent.step(state, action, reward, next_state, done)

        state = next_state
        score += reward 
        

        if done == True:
            break
    print(score)
    #time.sleep(10)
    env.save_to_plot()
    if reward >= 900:
        b +=1
print(b)
print("porcentagem de acerto = " + str(b/300))