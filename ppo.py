import gym
import torch
import torch.nn.functional as F
import numpy as np
import rl_utils
import torch.nn as nn

class policy_net(torch.nn.Module):

    def __init__(self,state_dim,action_dim,hidden_size):
        super().__init__()
        self.linear_1 = nn.Linear(state_dim,hidden_size)
        self.linear_2 = nn.Linear(hidden_size,action_dim)

    def forward(self,state):
        state = F.relu(self.linear_1(state))
        return F.softmax(self.linear_2(state),dim=1)
    
class value_net(nn.Module):

    def __init__(self,state_dim,hidden_size):
        super().__init__()
        self.linear_1 = nn.Linear(state_dim,hidden_size)
        self.linear_2 = nn.Linear(hidden_size,1)

    def forward(self,state):
        state = F.relu(self.linear_1(state))
        return self.linear_2(state)
    
class PPO:
    '''PPO算法，截断'''
    def __init__(self,state_dim,hidden_size,action_dim,actor_lr,critic_lr,
                 lmbda, num_epochs, eps, gamma, device):
        self.actor = policy_net(state_dim,action_dim,hidden_size).to(device)
        self.critic = value_net(state_dim,hidden_size)
        self.actor_optmizer = torch.optim.Adam(self.actor.parameters(),lr=actor_lr)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(),lr=critic_lr)
        self.gamma = gamma
        self.lmbda = lmbda
        self.num_epochs = num_epochs
        self.eps = eps
        self.device = device

    def take_action(self,state):
        state = torch.tensor([state],dtype=torch.float).to(self.device)
        probs = self.actor(state)
        print(f'probs.shape: {probs.shape}',probs.shape)
        action_dist = torch.distributions.Categorical(probs)
        action = action_dist.sample()
        return action.item()
    
    def update(self,transition_dict):
        states = torch.tensor(transition_dict['states'],dtype=torch.float).to(self.device)
        actions = torch.tensor(transition_dict['actions']).view(-1,1)