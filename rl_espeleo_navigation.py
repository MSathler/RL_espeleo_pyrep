from os.path import dirname, join, abspath
import time 
import numpy as np
from enviroment import ReacherEnv
from collections import deque
import torch
from agent import Agent
from model import hill_climbing_Policy, Reinforce_Policy
import matplotlib.pyplot as plt
import torch.optim as optim

EPISODES = 10000
EPISODE_LENGTH = int(50)
SCENE_FILE = join(dirname(abspath(__file__)), 'cenarios/espeleo.ttt')

env = ReacherEnv(SCENE_FILE,False)
agent = Agent(state_size=16, action_size=5, seed=0)
replay_buffer = []
# agent.qnetwork_local.load_state_dict(torch.load('dicionario_pth/checkpoint_05_05.pth'))
scores = []
mean = []
scores_window = deque(maxlen=100)
eps = 1.0
loss = []
t = 0

best = -9999.0


for e in range(1, EPISODES + 1):
    state = env.reset()
    rewards = []
    print('Starting episode %d' % e)
    score = 0
    if e >= 650:
        EPISODE_LENGTH = int(150)
    
    t = time.clock_gettime(time.CLOCK_MONOTONIC)
    for i in range(EPISODE_LENGTH):

        action = agent.act(state,eps) 

        done, reward, next_state = env.step(action)
        agent.step(state, action, reward, next_state, done)
        state = next_state
        score += reward 
            
        if done == True:
            break

    print("Tempo gasto no episodio: " + str(time.clock_gettime(time.CLOCK_MONOTONIC) - t))
    eps = max(0.01, 0.99*eps)
    scores_window.append(score)       
    if (np.mean(scores_window) > best) and (e >= 100):
        best = np.mean(scores_window)
    scores.append(score)
    mean.append(np.mean(scores_window))
    print(scores)
    print()
    print('\rEpisode {}\tAverage Score: {:.2f}\tBest Average: {:.2f} '.format(e, np.mean(scores_window), best), end="")
    if (np.mean(scores_window))>=best and (e>= 100.0):
            print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(e, np.mean(scores_window)))
            torch.save(agent.qnetwork_local.state_dict(), 'dicionario_pth/checkpoint_espeleo_posvar4x.pth')

    
    print('Reached target %d!' % i)


torch.save(agent.qnetwork_local.state_dict(), 'dicionario_pth/checkpoint_espeleo_posvar41x.pth')
env.shutdown()
plt.plot(np.linspace(0,EPISODES ,len(scores),endpoint=False), scores)

plt.plot(np.linspace(0,EPISODES ,len(mean),endpoint=False), mean)

plt.xlabel('Episode Number')
plt.ylabel('Average Reward (Over Next %d Episodes)')
plt.show()


            
