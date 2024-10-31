import numpy as np
import random
from constant import MOVES

class Sarsa:
    def __init__(self,env,alfa,gamma,eps):
        self.env = env
        self.alfa = alfa
        self.gamma = gamma
        self.eps = eps
        self.num_row, self.num_col = env.shape
        self.Q = np.zeros([env.size,4])
        self.pi = [[0.25,0.25,0.25] for _ in range(env.size)]

#    def reset(self):
    def reached(self, x, y):
        return x + y * (self.num_col) == (self.num_col * self.num_row -1)

    def take_action(self, x, y):
        p = random.random()
        if p <self.eps:
            return random.randint(0,3)
        else:
            return np.argmax(self.Q[x + y* self.num_col])
        
    def update(self,action,x,y,reward,x1,y1):
        action1 = self.take_action(x1, y1)
        td_error = reward + self.gamma * self.Q[x1+y1*self.num_col][action1]\
                                 - self.Q[x+y*self.num_col]
        self.Q[x+y*self.num_col] += self.alfa * td_error
        
    def is_valid(self, move, x, y):
        return x + move[0] >=0 and x + move[0] < self.num_col\
                and y + move[1] >= 0 and y + move[1] < self.num_row\
                and self.env[y+move[1],x+move[0]] != 1
    
    def move(self,action,x,y):
        
        p = random.random()
        if p < 0.1:
            move = MOVES[(action+1)%4]
            if not self.is_valid(move,x,y):
                # 留在原处
                return x,y,self.env[y,x]-1
            else:
                # 右
                x += move[0]
                y += move[1]
                return x,y,self.env[y,x]-1
        elif p < 0.2:
            move = MOVES[(action+3)%4]
            if not self.is_valid(move,x,y):
                # 留在原处
                return x,y,self.env[y,x]-1
            else:
                # 左
                x += move[0]
                y += move[1]
                return x,y,self.env[y,x]-1
        else:
            move = MOVES[action]
            if not self.is_valid(move,x,y):
                # 留在原处
                return x,y,self.env[y,x]-1
            else:
                # 前
                x += move[0]
                y += move[1]
                return x,y,self.env[y,x]-1

    def iteration(self,num_epoch):
        for _ in range(num_epoch):
            x, y = 0, 0
            while not self.reached(x, y):
                action = self.take_action(x, y)
                x1, y1, reward =  self.move(action, x, y)
                self.update(action,x,y,reward,x1,y1)
                x = x1
                y = y1
        return self.get_pi()

    def get_pi(self):
        qmax = np.amax(self.Q,axis=1)
        for i in range(qmax.size):
            cnt = sum(self.Q[i] == qmax[i])
            self.pi[i] = [1/cnt if self.Q[i][j]==qmax[i] else 0 for j in range(4)]
        return self.pi
