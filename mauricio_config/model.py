import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.distributions import Categorical
import random

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class QNetwork(nn.Module):

    def __init__(self, state_size, action_size, seed, fc1_units=64, fc2_units=64):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
            fc1_units (int): Number of nodes in first hidden layer
            fc2_units (int): Number of nodes in second hidden layer
        """
        super(QNetwork, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, fc1_units)
        self.fc2 = nn.Linear(fc1_units, fc2_units)
        self.fc3 = nn.Linear(fc2_units, action_size)

    def forward(self, state):
        """Build a network that maps state -> action values."""
        x = torch.tanh(self.fc1(state))
        x = torch.tanh(self.fc2(x))
        return self.fc3(x)


###########################################################################
class hill_climbing_Policy():

    def __init__(self, state_size=16, action_size=5):
        self.w = 1e-4*np.random.rand(state_size, action_size)  # weights for simple linear policy: state_space x action_space
        self.action_size = action_size
    def forward(self, state):
        x = np.dot(state, self.w)
        return np.exp(x)/sum(np.exp(x))
    
    def act(self, state, eps):
        probs = self.forward(state)
        #action = np.random.choice(2, p=probs) # option 1: stochastic policy option 2: deterministic policy

        if random.random() > eps:
            return np.argmax(probs) 
            
        else:
            return random.choice(np.arange(self.action_size))
        
#############################################################################



#############################################################################
class Reinforce_Policy(nn.Module):
    def __init__(self, state_size=16, action_size=5, h1_size=64,h2_size=64):
        super(Reinforce_Policy, self).__init__()
        self.fc1 = nn.Linear(state_size, h1_size)
        self.fc2 = nn.Linear(h1_size, action_size)
        self.action_size = action_size

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        
        return F.softmax(x, dim=1)
    
    def act(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)
        probs = self.forward(state).cpu()
        m = Categorical(probs)
        action = m.sample()
        # if random.random() > eps:
        return action.item(), m.log_prob(action)
            
        # else:
        #     return random.choice(np.arange(self.action_size)), m.log_prob(action)
#############################################################################