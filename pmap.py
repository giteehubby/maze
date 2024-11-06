import numpy as np
import random

MOVES = [(1,0),(0,1),(-1,0),(0,-1)]

def generate_pmap(width, height, max_block_num, s_x, s_y, f_x, f_y):
    max_block_num = min(height * width - 2, max_block_num)
    pmap = np.zeros((height, width),dtype=np.int8)
    n = 0
    while n < max_block_num:
        new_block = random.randint(0,height * width -1)
        if new_block == s_y * width + s_x or new_block == f_y * width + f_x:
            continue
        n_y = new_block // width
        n_x = new_block % width
        # print(n_x,n_y)
        if pmap[n_y][n_x] == 0:
            pmap[n_y, n_x] = 1
            if corner_linked(pmap, s_x, s_y, f_x, f_y):
                n += 1
                continue
            else:
                pmap[n_y, n_x] = 0
                break
    pmap[f_y,f_x] = 123 # 表示终点
    return pmap
        
def is_link(pmap, s_x, s_y, f_x, f_y):
    
    def dfs(x, y):
        if x == f_x and y == f_y:
            return True
        visited[y,x] = 1
        for move in MOVES:
            if is_valid(x, y, move):
                if dfs(x+move[0], y+move[1]):
                    return True
        # visited[y,x] = 0
        return False

    def is_valid(x, y, move):
        x += move[0]
        y += move[1]
        return x>=0 and x < pmap.shape[1]\
            and y >=0 and y < pmap.shape[0]\
            and visited[y,x]==0 and pmap[y,x]!=1
    
    visited = np.zeros_like(pmap)
    if pmap[s_y,s_x] == 1:
        return False
    return dfs(s_x,s_y)

def corner_linked(pmap, s_x, s_y, f_x, f_y):
    (height, width) = pmap.shape
    for f in [[1,1],[1,height-2],[width-2,1],[width-2,height-2],[f_x,f_y]]:
        if not is_link(pmap,s_x,s_y,*f):
            return False
    return True

def guarantee_roadnum(pmap, s_x, s_y, f_x, f_y, roadnum):
    def dfs(x, y, cnt):
        if x == f_x and y == f_y:
            cnt += 1
            return cnt
        visited[y,x] = 1
        for move in MOVES:
            if is_valid(x, y, move):
                cnt = dfs(x+move[0], y+move[1], cnt)
                if cnt >= roadnum:
                    return cnt

        visited[y,x] = 0
        return cnt

    def is_valid(x, y, move):
        x += move[0]
        y += move[1]
        return x>=0 and x < pmap.shape[1]\
            and y >=0 and y < pmap.shape[0]\
            and visited[y,x]==0 and pmap[y,x]!=1
    
    visited = np.zeros_like(pmap)
    cnt = 0
    if pmap[s_y,s_x] == 1:
        return False
    
    return dfs(s_x,s_y,cnt) 

def narrow(maze, s_x, s_y, f_x, f_y):
    height,width = maze.shape
    pattern = np.zeros((2,2),dtype=np.uint8)
    for i in range(height-1):
        for j in range(width-1):
            if np.bitwise_or(pattern,maze[i:i+2,j:j+2]).sum() == 0:
                p = random.randint(0,3)
                for _ in range(4):
                    maze[i+p//2][j+p%2] = 1
                    satisfy = True
                    if satisfy and is_link(maze, s_x, s_y, f_x, f_y):
                        break
                    maze[i+p//2][j+p%2] = 0
                    p = (p + 1) % 4
    return maze

def narrow1(maze, s_x, s_y, f_x, f_y):
    height,width = maze.shape
    pattern = np.zeros((2,2),dtype=np.int8)
    for i in range(0,height-1,2):
        for j in range(width-1):
            if np.bitwise_or(pattern,maze[i:i+2,j:j+2]).sum() == 0:
                p = random.randint(0,3)
                for _ in range(4):
                    maze[i+p//2][j+p%2] = 1
                    satisfy = True
                    if satisfy and is_link(maze, s_x, s_y, f_x, f_y):
                        break
                    maze[i+p//2][j+p%2] = 0
                    p = (p + 1) % 4
    for i in range(1,height-1,2):
        for j in range(0,width-1,2):
            if np.bitwise_or(pattern,maze[i:i+2,j:j+2]).sum() == 0:
                p = random.randint(0,3)
                for _ in range(4):
                    maze[i+p//2][j+p%2] = 1
                    satisfy = True
                    if satisfy and is_link(maze, s_x, s_y, f_x, f_y):
                        break
                    maze[i+p//2][j+p%2] = 0
                    p = (p + 1) % 4
    return maze

def narrow2(maze, s_x, s_y, f_x, f_y):
    height,width = maze.shape
    pattern = np.zeros((2,2),dtype=np.uint8)
    for i in range(height-1):
        for j in range(width-1):
            if np.bitwise_or(pattern,maze[i:i+2,j:j+2]).sum() == 0:
                p = 0
                for _ in range(4):
                    maze[i+p//2][j+p%2] = 1
                    satisfy = True
                    if satisfy and is_link(maze, s_x, s_y, f_x, f_y):
                        break
                    maze[i+p//2][j+p%2] = 0
                    p = (p + 1) % 4
    
    return maze

def narrow3(maze, s_x, s_y, f_x, f_y):
    height,width = maze.shape
    pattern = np.zeros((2,2),dtype=np.uint8)
    for i in range(height-1):
        for j in range(width-1):
            if np.bitwise_or(pattern,maze[i:i+2,j:j+2]).sum() == 0:
                for _ in range(4):
                    p = random.randint(0,3)
                    maze[i+p//2][j+p%2] = 1
                    if corner_linked(maze, s_x, s_y, f_x, f_y):
                        break
                    maze[i+p//2][j+p%2] = 0
                    p = (p + 1) % 4
    
    return maze

def trap(maze, s_x, s_y, f_x, f_y,num_trap=4):
    i = 0
    height,width = maze.shape
    while i < num_trap:
        trap_block = random.randint(0,height * width -1)
        if trap_block == s_x * width + s_y or trap_block == f_x * width + f_y:
            continue
        n_y = trap_block // width
        n_x = trap_block % width
        if maze[n_y][n_x] == 0:
            maze[n_y, n_x] = random.randint(-18,-1)
            i += 1
    return maze