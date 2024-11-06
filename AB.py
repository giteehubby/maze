from solver import MOVES
import random

def movep(p,move):
    return [p[0] + move[0], p[1] + move[1]]
    
def recoverp(p,move):
    return [p[0] - move[0], p[1] - move[1]]

class Alfa_Beta_Search:
    def __init__(self,max_h):
        self.step = 0
        self.max_h = max_h
        self.jerry_path = []
        self.tom_path = []
        
    def search(self,jerry_p,tom_p,desti_p,maze):
        self.desti_p = desti_p
        self.maze = maze
        while True:
            self.jerry_path.append(jerry_p)
            self.tom_path.append(tom_p)
            v,move = self.max_v(jerry_p,tom_p,-1e8,1e8,0)
            if move is None:
                break
            jerry_p = movep(jerry_p,move)
            while True:
                rn = random.randint(0,3)
                rm = MOVES[rn]
                if self.is_valid(*tom_p,rm):
                    tom_p = movep(tom_p,rm)
                    break
        return self.jerry_path,self.tom_path

    def is_valid(self, x, y, move):
        x += move[0]
        y += move[1]
        return x>=0 and x < self.maze.shape[1]\
            and y >=0 and y < self.maze.shape[0]\
            and self.maze[y,x] != 1

    def is_terminal(self,jerry_p,tom_p,recursive_h):
        return recursive_h >= self.max_h or \
                [*tom_p] == [*jerry_p] or \
                [*jerry_p] == [*self.desti_p]
    
    def ultility(self,jerry_p,tom_p,recursive_h):
        def manhaton(p1,p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        if recursive_h >= self.max_h:
            return -manhaton(jerry_p,self.desti_p) - 1/(manhaton(jerry_p,tom_p)+0.01) 
        elif tom_p == jerry_p:
            return -1e4
        elif jerry_p == self.desti_p:
            return 1e4
        
    def max_v(self,jerry_p,tom_p,alfa,beta,recursive_h):
        if self.is_terminal(jerry_p,tom_p,recursive_h):
            return self.ultility(jerry_p,tom_p,recursive_h),None
        v, bestmove = -1e8, None
        for move in MOVES:
            if not self.is_valid(*jerry_p,move):
                continue
            jerry_p = movep(jerry_p,move)
            v2,a = self.min_v(jerry_p,tom_p,alfa,beta,recursive_h+1)
            print('v2:'+str(v2))
            if v2 is None:
                v2 = 0
            if v2 > v:
                v = v2
                bestmove = move
                alfa = max(alfa,v)
            if v >= beta:
                return v,bestmove #其他被剪枝
            jerry_p = recoverp(jerry_p,move)
        return v,bestmove

    def min_v(self,jerry_p,tom_p,alfa,beta,recursive_h):
        if self.is_terminal(jerry_p,tom_p,recursive_h):
            return self.ultility(jerry_p,tom_p,recursive_h),None
        v, bestmove = 1e8, None
        for move in MOVES:
            if not self.is_valid(*tom_p,move):
                continue
            tom_p = movep(tom_p,move)
            v2,a = self.max_v(jerry_p,tom_p,alfa,beta,recursive_h+1)
            if v2 < v:
                v = v2
                bestmove = move
                beta = min(beta,v)
            if v <= alfa:
                return v,bestmove #其他被剪枝
            tom_p = recoverp(tom_p,move)
        return v,bestmove