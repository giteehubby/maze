import tkinter as tk
from tkinter import ttk
  
import time
from solver import dfs_solver,bfs_solver,unicost_solver,greedy_solver,Astar_solver
from pmap import generate_pmap,narrow,narrow2,narrow3,is_link
from TJ import Jerry
from pmap import random
  
# 定义迷宫的大小  
MAZE_SIZE = (28, 20)  
CELL_SIZE = 20
MOVES = [(1,0),(0,1),(-1,0),(0,-1)]

# 定义起点和终点  
start = (0, 0)
end = (27, 19)

maze = generate_pmap(*MAZE_SIZE, 1000, *start, *end)
maze = narrow3(maze, *start, *end,2)
  
jerry = Jerry(*start)
while True:
    p = random.randint(0,MAZE_SIZE[1] * MAZE_SIZE[0] -1)
    if p == start[0] * start[1] or (not(is_link(maze,*start,p%MAZE_SIZE[1],p//MAZE_SIZE[0]))):
        continue
    else:
        tom = Jerry(p%MAZE_SIZE[1],p//MAZE_SIZE[0],'blue')
        break


# 初始化tkinter窗口  
root = tk.Tk()  
root.title("迷宫动画")



# 创建画布  
canvas = tk.Canvas(root, width=CELL_SIZE * MAZE_SIZE[0], height=CELL_SIZE * MAZE_SIZE[1])  
canvas.pack()  
  
# 绘制迷宫  
def draw_maze():  
    for y in range(MAZE_SIZE[1]):  
        for x in range(MAZE_SIZE[0]):  
            if maze[y][x] == 0:  
                canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="white", outline="black")  
            else:  
                canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="black", outline="black")  
  
def animate_path(road,id=None):  
        if road:  
            x, y = road.pop(0)
            if id is not None:
                # pass
                canvas.delete(id)
            id = canvas.create_oval(x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE + CELL_SIZE // 4,  
                               (x + 1) * CELL_SIZE - CELL_SIZE // 4, (y + 1) * CELL_SIZE - CELL_SIZE // 4, fill="red")
            root.after(500, lambda :animate_path(road,id))  # 500毫秒后调用自己  
        else:  
            # 可以在这里添加到达终点的处理，比如显示一个消息或改变终点颜色  
            print("到达终点！")

draw_maze()
# dfs_obj = dfs_solver()
# path = dfs_obj.solve(maze, *start, *end)
# dfs_obj.animate_path()

# bfs_obj = bfs_solver()
# path = bfs_obj.solve(maze, *start, *end)
# print(path)

# unico_obj = unicost_solver()
# path = unico_obj.solve(maze, *start, *end)
# print(path)
# animate_path(path)

# greed_obj = greedy_solver()
# path = greed_obj.solve(maze, *start, *end)
# print(path)
# animate_path(path)

tom.update(canvas)

astar_obj = greedy_solver()
path = astar_obj.solve(maze, *start, *end)
print(path)
animate_path(path)

def on_key_press(event,jerry):  
    if event.keysym == 'Up':
        move = (-1,0)
    elif event.keysym == 'Down':
        move = (1,0)
    elif event.keysym == 'Left':
        move = (0,-1)
    elif event.keysym == 'Right':
        move = (0,1)
    else:
        return
    if jerry.can_move(move,maze):
        jerry.move(move)
    jerry.update(canvas)
 
  
#绑定键盘事件
root.bind("<KeyPress>", lambda event:on_key_press(event,jerry))
# jerry.update(canvas)
# 运行tkinter主循环  
root.mainloop()