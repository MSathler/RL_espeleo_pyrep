import numpy as np
from collections import defaultdict
import random


class Agent:

    def __init__(self, env, nA=6):
        """ Initialize agent.

        Params
        ======
        - nA: number of actions available to the agent
        """
 ################################## Modifiquei ############################################
        self.env = env
 ################################## Modifiquei ############################################
        self.nA = nA
        self.Q = defaultdict(lambda: np.zeros(self.nA))

    def select_action(self, state, eps):
        """ Given the state, select an action.

        Params
        ======
        - state: the current state of the environment

        Returns
        =======
        - action: an integer, compatible with the task's action space
        """
        
        #return np.random.choice(self.nA) Default
        
################################## Modifiquei ############################################
        if random.random() > eps: # select greedy action with probability epsilon
            return np.argmax(self.Q[state])
        else:                     # otherwise, select an action randomly
            return random.choice(np.arange(self.env.action_space.n))
################################## Modifiquei ############################################
       
        
    def step(self, state, action, reward, next_state, done, alpha = 0.5, gamma = 1.0): # quanto maior o alpha mais rapid converge neste caso
        """ Update the agent's knowledge, using the most recently sampled tuple.

        Params
        ======
        - state: the previous state of the environment
        - action: the agent's previous choice of action
        - reward: last reward received
        - next_state: the current state of the environment
        - done: whether the episode is complete (True or False)
        """
        #self.Q[state][action] += 1  Default
        
        ################################## Modifiquei ############################################
        current = self.Q[state][action]  # estimate in Q-table (for current state, action pair)
        Qsa_next = np.max(self.Q[next_state]) if next_state is not None else 0  # value of next state
        target = reward + (gamma * Qsa_next) 
        self.Q[state][action] = current + (alpha * (target - current))
        ################################## Modifiquei ############################################
        