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

EPISODES = 100000
EPISODE_LENGTH = int(50)
SCENE_FILE = join(dirname(abspath(__file__)), 'p3dx_scene_pompy.ttt')

env = ReacherEnv(SCENE_FILE)
agent = Agent(state_size=21, action_size=5, seed=0)
replay_buffer = []
# agent.qnetwork_local.load_state_dict(torch.load('checkpoint_al_28_01_12.pth'))
scores = []
mean = []
scores_window = deque(maxlen=100)
eps = 1.0 
loss = []
t = 0

best = -9999.0

# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# #policy = hill_climbing_Policy() ## hill clibing
# policy = Reinforce_Policy().to(device)
# gamma = 0.99
# noise_scale=1e-2
# best_R = -np.Inf
# optimizer = optim.Adam(policy.parameters(), lr=1.2e-2)

######################   hill climbimb   ######################
# for e in range(1, EPISODES + 1):
#     state = env.reset()
#     rewards = []
#     print('Starting episode %d' % e)
#     score = 0


    # for t in range(EPISODE_LENGTH):
    #     action = policy.act(state)
    #     done, reward, next_state= env.step(action)
    #     rewards.append(reward)
    #     if done:
    #         break 
        
    # scores_window.append(sum(rewards))
    # scores.append(sum(rewards))

    # discounts = [gamma**i for i in range(len(rewards)+1)]
    # R = sum([a*b for a,b in zip(discounts, rewards)])

    # if R >= best_R: # found better weights
    #     best_R = R
    #     best_w = policy.w
    #     noise_scale = max(1e-3, ; / 2)
    #     policy.w += noise_scale * np.random.rand(*policy.w.shape) 
    # else: # did not find better weights
    #     noise_scale = min(2, noise_scale * 2)
    #     policy.w = best_w + noise_scale * np.random.rand(*policy.w.shape)

    # if e % 100 == 0:
    #     print('Episode {}\tAverage Score: {:.2f}'.format(e, np.mean(scores_window)))
    # if np.mean(scores_window)>=1000.0:
    #     print('Environment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(e-100, np.mean(scores_window)))
    #     policy.w = best_w
    #     break
    # print(scores)

######################   hill climbimb   ###################### END


######################     Reinforce     ######################
# for i_episode in range(1, EPISODES+1):
#     if i_episode == 1500:
#         optimizer = optim.Adam(policy.parameters(), lr=0.5e-3)
#     saved_log_probs = []
#     rewards = []
#     print('Starting episode %d' % i_episode)
#     state = env.reset()
#     for t in range(EPISODE_LENGTH):
#         action, log_prob = policy.act(state)
#         saved_log_probs.append(log_prob)
#         done, reward, next_state = env.step(action)
#         rewards.append(reward)
#         if done:
#             break 
#     # eps = max(0.01, 0.99*eps)
#     scores_window.append(sum(rewards))
#     scores.append(sum(rewards))
        
#     discounts = [gamma**i for i in range(len(rewards)+1)]
#     R = sum([a*b for a,b in zip(discounts, rewards)])
#     policy_loss = []
#     for log_prob in saved_log_probs:
#         policy_loss.append(-log_prob * R)
#     policy_loss = torch.cat(policy_loss).sum()
        
#     optimizer.zero_grad()
#     policy_loss.backward()
#     optimizer.step()
        
    
#     if np.mean(scores_window)>=1000.0:
#         print('Environment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)))
#         break
#     print(scores)
#     print()
#     print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)), end="")
#     print()

######################     Reinforce     ###################### END


######################  DEEP Q-LEARNING  ######################
for e in range(1, EPISODES + 1):
    state = env.reset()
    rewards = []
    print('Starting episode %d' % e)
    score = 0

    for i in range(EPISODE_LENGTH):

        action = agent.act(state,eps) 

        done, reward, next_state = env.step(action)
        agent.step(state, action, reward, next_state, done)

        state = next_state
        score += reward 
            

        if done == True:
            break

    eps = max(0.01, 0.99*eps)
    scores_window.append(score)       # save most recent score
    if np.mean(scores_window) > best:
        best = np.mean(scores_window)
    scores.append(score)
    mean.append(np.mean(scores_window))
    print(scores)
    print()
    print('\rEpisode {}\tAverage Score: {:.2f}\tBest Average: {:.2f} '.format(e, np.mean(scores_window), best), end="")
    if (np.mean(scores_window))>=best:
            print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(e, np.mean(scores_window)))
            torch.save(agent.qnetwork_local.state_dict(), 'checkpoint_al_28_01_12.pth')

    
    print('Reached target %d!' % i)
######################  DEEP Q-LEARNING  ###################### END    

torch.save(agent.qnetwork_local.state_dict(), 'checkpoint_tt2.pth')
env.shutdown()
plt.plot(np.linspace(0,EPISODES ,len(scores),endpoint=False), scores)

plt.plot(np.linspace(0,EPISODES ,len(mean),endpoint=False), mean)

plt.xlabel('Episode Number')
plt.ylabel('Average Reward (Over Next %d Episodes)')
plt.show()





# ############################# Teste file ##############################
# agent.qnetwork_local.load_state_dict(torch.load('checkpoint_11_01.pth'))
# b = 0
# for i in range(1,101):
#     state = env.reset()
#     score = 0
#     for j in range(150):
#         action = agent.act(state)

#         done, reward, next_state = env.step(action)
#         agent.step(state, action, reward, next_state, done)

#         state = next_state
#         score += reward 
        

#         if done == True:
#             break
#     print(score)
#     if reward >= 1000:
#         b +=1
# print("porcentagem de acerto = " + str(b))



            
