import numpy as np
import matplotlib.pyplot as plt
import random
class bernouliBandit:
    # 多臂老虎机
    def __init__(self,num_arm):
        self.probabilities = np.random.uniform(0,1,size=num_arm)
        self.most_idx = np.argmax(self.probabilities)
        self.most_p = self.probabilities[self.most_idx]
        self.num_arm = num_arm

    def step(self,i):
        if random.random() < self.probabilities[i]:
            return 1
        return 0
    
# np.random.seed(1)
k = 10
bandit = bernouliBandit(k)
print(f'最好的老虎臂:{bandit.most_idx}, 最大的可能性:{bandit.most_p}')
print('probabilities:',bandit.probabilities)

class solver:
    def __init__(self,bandit):
        self.bandit = bandit
        self.counts = np.zeros(self.bandit.num_arm)
        self.accumulate_regret = 0
        self.action_seq = []
        self.regrets = []

    def step(self):
        raise NotImplementedError
    
    def run(self,num_steps):
        for _ in range(num_steps):
            k, result = self.step()
            self.action_seq.append(k)
            self.counts[k] += 1
            self.accumulate_regret += (self.bandit.most_p - result)
            # self.accumulate_regret += (self.bandit.most_p - self.bandit.probabilities[k])
            self.regrets.append(self.accumulate_regret)

class epsGreedy(solver):
    def __init__(self,bandit,eps=0.01):
        super().__init__(bandit)
        self.eps = eps
        self.estimate = np.ones(self.bandit.num_arm)

    def step(self):
        if np.random.random() < self.eps:
            k = random.randint(0,self.bandit.num_arm - 1)
        k = np.argmax(self.estimate)
        result = self.bandit.step(k)
        self.estimate[k] += (result - self.estimate[k])/(self.counts[k] + 1)
        return k,result

def plot_results(solver_regrets,solver_names,num_arm):
    for i,regret in enumerate(solver_regrets):
        time_list = list(range(len(regret)))
        plt.plot(time_list,regret,label=solver_names[i])
    plt.xlabel('Time steps')
    plt.ylabel('regrets')
    plt.title('%d-armed bandit' % num_arm)
    plt.legend()
    plt.show()

# eps_greedy_solver = epsGreedy(bandit)
# eps_greedy_solver.run(500)
# plot_results([eps_greedy_solver.regrets],['epsGreedy'],10)
# print(eps_greedy_solver.regrets)
# print(eps_greedy_solver.action_seq)
# print('estimate: ',eps_greedy_solver.estimate)

epslons = [1e-4,1e-3,0.01,0.1,0.25,0.5]
regrets = []
solver_names = []
for i, eps in enumerate(epslons):
    solver = epsGreedy(bandit,eps)
    solver.run(5000)
    regrets.append(solver.regrets)
    solver_names.append('eps={}'.format(epslons[i]))

plot_results(regrets,solver_names,k)


class decay_epsGreedy(solver):
    def __init__(self, bandit, **kwargs):
        super().__init__(bandit)
        self.estimate = np.ones(self.bandit.num_arm)
        self.step_count = 0

    def step(self):
        self.step_count += 1
        if np.random.random() < 1 / self.step_count:
            k = random.randint(0, self.bandit.num_arm - 1)
        k = np.argmax(self.estimate)
        result = self.bandit.step(k)
        self.estimate[k] += (result - self.estimate[k]) / (self.counts[k] + 1)
        return k, result


class simulate_anneal(solver):
    def __init__(self, bandit, **kwargs):
        super().__init__(bandit)
        self.estimate = np.ones(self.bandit.num_arm)
        self.step_count = 0

    def step(self):
        self.step_count += 1
        k = random.randint(0, self.bandit.num_arm - 1)
        bk = np.argmax(self.estimate)
        if k != bk and np.random.random() > np.exp((self.estimate[k] - self.estimate[bk]) / self.step_count):
            k = bk
        result = self.bandit.step(k)
        self.estimate[k] += (result - self.estimate[k]) / (self.counts[k] + 1)
        return k, result

# dec_eps_solver = decay_epsGreedy(bandit)
# sia_solver = simulate_anneal(bandit)
# dec_eps_solver.run(5000)
# sia_solver.run(5000)
# print('dec的累积懊悔:',dec_eps_solver.accumulate_regret)
# print('sia的累积懊悔:',sia_solver.accumulate_regret)
# plot_results([dec_eps_solver.regrets,sia_solver.regrets],['dec','sia'],10)