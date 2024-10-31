import copy

MOVES = [(1,0),(0,1),(-1,0),(0,-1)]

class Value_Iteration:

    def __init__(self,env,gamma,theta):
        self.env = env
        self.gamma = gamma
        self.theta = theta
        self.n_row, self.n_col = env.shape
        self.pi = [[0.25,0.25,0.25,0.25] for i in range(self.n_row*self.n_col)]
        self.V = [0] * (self.n_col * self.n_row)
        self.env[self.n_row-1][self.n_col-1] = 100

    def is_valid(self,i,mi):
        p_ = self.move(i,mi)
        return p_[0] >= 0 and p_[0] < self.n_col\
                and p_[1] >= 0 and p_[1] < self.n_row\
                and self.env_p(p_) != 1
    
    def to_xy(self,i):
        # 将i转化为坐标
        return [i%self.n_col,i//self.n_col]
    
    def to_i(self,p):
        return p[0] + p[1] * self.n_col
    
    def env_p(self,p):
        return self.env[p[1],p[0]]
    
    def move(self,i,mi):
        move = MOVES[mi]
        p = self.to_xy(i) # [x,y]
        return [p[0]+move[0],p[1]+move[1]]
    
    def is_wall(self,i):
        p = self.to_xy(i)
        return self.env[p[1],p[0]] == 1
    
    def reward(self,i,mi):
        v = 0
        if self.is_valid(i,mi): #检查能不能走
            v += 0.8 * self.env_p(self.move(i,mi)) #前
            v += 0.8 * self.gamma * self.V[self.to_i(self.move(i,mi))]
        else:
            v += 0.8 * self.gamma * self.V[i] # 留在原地

        if self.is_valid(i,(mi+1)%4):
            v += 0.1 * self.env_p(self.move(i,(mi+1)%4)) #右
        else:
            v += 0.1 * self.gamma * self.V[i]

        if self.is_valid(i,(mi+3)%4):
            v += 0.1 * self.env_p(self.move(i,(mi+3)%4)) #左
        else:
            v += 0.1 * self.gamma * self.V[i]
 
        return v - 1


    def value_iteration(self):
        cnt = 0
        while True:
            deta = 0
            new_V = [0] * (self.n_col * self.n_row)
            for i in range(len(self.V) - 1):
                if self.is_wall(i):
                    continue
                v = -1e8
                for mi in range(4): #四个方向
                    # 每个方向都有三种可能的结果
                    v = max(v, self.reward(i,mi))
                new_V[i] = v
                deta = max(deta,abs(v-self.V[i]))
            self.V = new_V
            cnt += 1
            if deta < self.theta:
                break
        print('策略评估%d轮后完成'%cnt)
        return self.get_policy()

    
    def get_policy(self):
        for i in range(self.n_col * self.n_col-1): #终点不参与策略迭代
            if self.is_wall(i):
                continue
            qsa_list = []
            for j in range(4):
                qsa_list.append(self.reward(i,j))
            maxq = max(qsa_list)
            cnt = qsa_list.count(maxq)
            self.pi[i] = [1/cnt if qsa_list[j]==maxq else 0 for j in range(4)]
        print('策略提升完成')
        return self.pi