# from lose_palace import MOVES,CELL_SIZE
import tkinter as tk
import numpy as np
from constant import MOVES

MAZE_SIZE = (30, 20)  
CELL_SIZE = 20

class solver:
    def __init__(self):
        self.road = []
        self.id = None
        self.f_x = None
        self.f_y = None
        self.maze = None

    def solve(self):
        raise NotImplementedError
    
    def h(self,x,y):
        if self.f_x is None or self.f_y is None:
            return TypeError('destination unknow')
        return abs(self.f_x - x) + abs(self.f_y - y)
    
    def is_valid(self,x, y, move,visited=None):
        x += move[0]
        y += move[1]
        if visited is None:
            return x>=0 and x < self.maze.shape[1]\
                and y >=0 and y < self.maze.shape[0]\
                and self.maze[y,x] != 1
        return x>=0 and x < self.maze.shape[1]\
            and y >=0 and y < self.maze.shape[0]\
            and visited[y,x]==False and self.maze[y,x] != 1
    
    def goal_test(self,x,y):
        return x == self.f_x and y == self.f_y


class dfs_solver(solver):
    def __init__(self):
        super().__init__()
        pass

    def solve(self, maze, s_x, s_y, f_x, f_y):
        self.f_x = f_x
        self.f_y = f_y

        def dfs(x, y):
            if x == f_x and y == f_y:
                self.road.append([x,y])
                return True
            visited[y,x] = 1
            self.road.append([x,y])
            for move in MOVES:
                if is_valid(x, y, move):
                    if dfs(x+move[0], y+move[1]):
                        return True
            self.road.pop()
            return False

        def is_valid(x, y, move):
            x += move[0]
            y += move[1]
            return x>=0 and x < maze.shape[1]\
                and y >=0 and y < maze.shape[0]\
                and visited[y,x]==False and maze[y,x] != 1

        visited = np.zeros_like(maze,dtype=np.bool_)
        dfs(s_x, s_y)
        return self.road

class bfs_solver(solver):
    def __init__(self):
        super().__init__()
        self.roadqueue = []
        pass

    def solve(self, maze, s_x, s_y, f_x, f_y):
        self.f_x = f_x
        self.f_y = f_y
        self.roadqueue = []

        def is_valid(x, y, move):
            x += move[0]
            y += move[1]
            return x>=0 and x < maze.shape[1]\
                and y >=0 and y < maze.shape[0]\
                and visited[y,x]==False and maze[y,x] != 1

        visited = np.zeros_like(maze,dtype=np.bool_)
        self.roadqueue.append([s_x,s_y])

        while self.roadqueue:
            x,y = self.roadqueue.pop(0)
            visited[y,x] = 1
            
            for move in MOVES:
                if is_valid(x, y, move) and [x+move[0],y+move[1]] not in self.roadqueue:
                    
                    if self.goal_test(x+move[0],y+move[1]):
                        self.road.insert(0,[x+move[0],y+move[1]])
                        return self.solve(maze,s_x,s_y,x,y)
                    self.roadqueue.append([x+move[0],y+move[1]])


        return self.road

class road_pt:
    def __init__(self,x,y,cost):
        self.x = x
        self.y = y
        self.cost = cost

    def __lt__(self, other):  
        return self.cost < other.cost

class unicost_solver(solver):
    def __init__(self):
        super().__init__()
        self.cost = {}
        self.roadqueue = []
        pass

    def solve(self, maze, s_x, s_y, f_x, f_y):
        self.f_x = f_x
        self.f_y = f_y
        self.roadqueue = []
        curcost = 0

        def is_valid(x, y, move):
            x += move[0]
            y += move[1]
            return x>=0 and x < maze.shape[1]\
                and y >=0 and y < maze.shape[0]\
                and visited[y,x]==False and maze[y,x] != 1

        visited = np.zeros_like(maze,dtype=np.bool_)
        self.roadqueue.append(road_pt(s_x,s_y,curcost))
        self.cost[(s_x,s_y)] = curcost

        while self.roadqueue:
            pt = self.roadqueue.pop(0)
            x = pt.x
            y = pt.y
            if pt.cost != self.cost[(x,y)]:
                continue
            visited[y,x] = 1
            curcost += 1
            for move in MOVES:
                if is_valid(x, y, move):
                    if (x+move[0],y+move[1]) in self.cost:
                        if curcost + 1 < self.cost[x+move[0],y+move[1]]:
                            self.cost[x+move[0],y+move[1]] = curcost + 1
                            self.roadqueue.append(road_pt(x+move[0],y+move[1],curcost + 1))
                        #else:

                    else:
                        self.cost[x+move[0],y+move[1]] = curcost + 1
                        self.roadqueue.append(road_pt(x+move[0],y+move[1],curcost + 1))
                    if self.goal_test(x+move[0],y+move[1]):
                        self.road.insert(0,[x+move[0],y+move[1]])
                        return self.solve(maze,s_x,s_y,x,y)
                    self.roadqueue.append(road_pt(x+move[0],y+move[1],curcost+1))

        return self.road
    
class greedy_solver(solver):
    def __init__(self):
        super().__init__()
        self.f_x,self.f_y = None, None

    
    
    def solve(self, maze, s_x, s_y, f_x, f_y):
        self.f_x = f_x
        self.f_y = f_y
        self.maze = maze
        def gdfs(x, y):
            if x == f_x and y == f_y:
                self.road.append([x,y])
                return True
            visited[y,x] = 1
            self.road.append([x,y])
            H = []
            i = 0
            for move in MOVES:
                if self.is_valid(x, y, move,visited):
                    H.append([i,self.h(x + move[0],y + move[1])])
                i += 1
            idx = [x[0] for x in sorted(H,key=lambda x:x[1])]
            for i in idx:
                if gdfs(x + MOVES[i][0], y + MOVES[i][1]):
                    return True
            self.road.pop()
            return False


        visited = np.zeros_like(maze,dtype=np.bool_)
        gdfs(s_x, s_y)
        return self.road
    
class Astar_solver(solver):
    def __init__(self):
        super().__init__()
        self.f_x, self.f_y = None, None
        self.cost = {}
        

    def solve(self, maze, s_x, s_y, f_x, f_y):
        self.f_x = f_x
        self.f_y = f_y
        self.roadqueue = []
        curcost = 0
        self.maze = maze

        def is_valid(x, y, move):
            x += move[0]
            y += move[1]
            return x>=0 and x < maze.shape[1]\
                and y >=0 and y < maze.shape[0]\
                and visited[y,x]==False and maze[y,x] != 1

        visited = np.zeros_like(maze,dtype=np.bool_)
        self.roadqueue.append(road_pt(s_x,s_y,curcost))
        self.cost[(s_x,s_y)] = curcost

        while self.roadqueue:
            pt = self.roadqueue.pop(0)
            x = pt.x
            y = pt.y
            if pt.cost != self.cost[(x,y)]:
                continue
            visited[y,x] = 1
            curcost += 1
            for move in MOVES:
                if is_valid(x, y, move):
                    if (x+move[0],y+move[1]) in self.cost:
                        if curcost + 1 < self.cost[x+move[0],y+move[1]]:
                            self.cost[x+move[0],y+move[1]] = curcost + 1
                            self.roadqueue.append(road_pt(x+move[0],y+move[1],curcost + 1 + self.h(x+move[0],y+move[1])))
                        #else:

                    else:
                        self.cost[x+move[0],y+move[1]] = curcost + 1
                        self.roadqueue.append(road_pt(x+move[0],y+move[1],curcost + 1))
                    if self.goal_test(x+move[0],y+move[1]):
                        self.road.insert(0,[x+move[0],y+move[1]])
                        return self.solve(maze,s_x,s_y,x,y)
                    self.roadqueue.append(road_pt(x+move[0],y+move[1],curcost+1))

        return self.road
