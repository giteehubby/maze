import tkinter as tk  
from tkinter import messagebox  
from pmap import generate_pmap,narrow3,is_link,trap
import numpy as np
from solver import greedy_solver, Astar_solver, dfs_solver, bfs_solver, unicost_solver
from AB import Alfa_Beta_Search
from random import randint
from TJ import Jerry
from policy_iteration import Policy_Iteration
from value_iteration import Value_Iteration
from sarsa import Sarsa

mapready = False
start = [0, 0]
num_col = 1
num_row = 1
end = [num_col-1, num_row-1]
maze = np.zeros((num_col,num_row),dtype= np.uint8)
have_tom = False
pi = None
polies = []

def animate_path(road,id=None,tom_road=None,id1=None):
    if tom_road is None:
        if road:
            canvas_width = canvas.winfo_width()  
            canvas_height = canvas.winfo_height()  
            cell_width = (canvas_width) // num_col
            cell_height = (canvas_height) // num_row
    
            x, y = road.pop(0)
            if id is not None:
                # pass
                canvas.delete(id)
            id = canvas.create_oval(x * cell_width + cell_width // 4, y * cell_height + cell_height // 4,  
                               (x + 1) * cell_width - cell_width // 4, (y + 1) * cell_height - cell_height // 4, fill="red")
            root.after(500, lambda :animate_path(road,id))  # 500毫秒后调用自己  
        else:  
            # 可以在这里添加到达终点的处理，比如显示一个消息或改变终点颜色  
            print("到达终点！")
    else:
        if road:
            canvas_width = canvas.winfo_width()  
            canvas_height = canvas.winfo_height()  
            cell_width = (canvas_width) // num_col
            cell_height = (canvas_height) // num_row
    
            x, y = road.pop(0)
            x_1, y_1 = tom_road.pop(0)
            if id is not None:
                # pass
                canvas.delete(id)
            if id1 is not None:
                # pass
                canvas.delete(id1)
            id = canvas.create_oval(x * cell_width + cell_width // 4, y * cell_height + cell_height // 4,  
                               (x + 1) * cell_width - cell_width // 4, (y + 1) * cell_height - cell_height // 4, fill="red")
            id1 = canvas.create_oval(x_1 * cell_width + cell_width // 4, y_1 * cell_height + cell_height // 4,  
                               (x_1 + 1) * cell_width - cell_width // 4, (y_1 + 1) * cell_height - cell_height // 4, fill="blue")
            root.after(500, lambda :animate_path(road,id,tom_road,id1))  # 500毫秒后调用自己  
        else:  
            # 可以在这里添加到达终点的处理，比如显示一个消息或改变终点颜色  
            print("到达终点！")

def on_button1_click():  
    dfs_obj = dfs_solver()
    path = dfs_obj.solve(maze, *start, *end)
    animate_path(path)
    step_label.config(text=f'宽度优先花费步数:{len(path)}')
  
def on_button2_click():  
    bfs_obj = bfs_solver()
    path = bfs_obj.solve(maze, *start, *end)
    animate_path(path)
    step_label.config(text=f'广度优先花费步数:{len(path)}')

def on_button3_click():
    unico_obj = unicost_solver()
    path = unico_obj.solve(maze, *start, *end)
    animate_path(path)
    step_label.config(text=f'一致代价花费步数:{len(path)}')
    pass

def on_button4_click():
    greedy_obj = greedy_solver()
    path = greedy_obj.solve(maze, *start, *end)
    print(path)
    animate_path(path)
    step_label.config(text=f'贪心算法花费步数:{len(path)}')

def on_button5_click():  
    astar_obj = Astar_solver()
    path = astar_obj.solve(maze, *start, *end)
    print(path)
    animate_path(path)
    step_label.config(text=f'A*算法花费步数:{len(path)}')

def on_button_mix_click():
    if not mapready:
        return
    while True:
        p = randint(0,num_col * num_row -1)
        if p == start[0] * start[1] or (not(is_link(maze,*start,p%num_col,p//num_col))):
            continue
        else:
            tom_p = [p%num_col,p//num_col]
            break
    ab_search = Alfa_Beta_Search(5)
    road,tom_road = ab_search.search(start,tom_p,(num_col-1,num_row-1),maze)
    animate_path(road,None,tom_road)

def on_button_pi_iter_click():
    policy_iter = Policy_Iteration(maze,gamma=0.618,theta=0.01)
    global pi
    pi = policy_iter.policy_iteration()
    draw_pi(pi[:-1])

def on_button_value_iter_click():
    value_iter = Value_Iteration(maze,gamma=0.618,theta=0.01)
    global pi
    pi = value_iter.value_iteration()
    draw_pi(pi[:-1])

def on_button_sarsa_click():
    sarsa_iter = Sarsa(maze,alfa=0.88,gamma=0.618,eps=0.1)
    global pi
    pi = sarsa_iter.iteration(500)
    draw_pi(pi[:-1])
    

    

def draw_maze():
    print(maze)
    canvas_width = canvas.winfo_width()  
    canvas_height = canvas.winfo_height()  
    # 计算每个单元格的尺寸（不包括padding）  
    cell_width = (canvas_width) // num_col
    cell_height = (canvas_height) // num_row
    for y in range(num_row):  
        for x in range(num_col):  
            if maze[y][x] == 0:  
                canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, 
                                        fill="white", outline="black")  
            elif maze[y][x] == 1:  
                canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, 
                                        fill="black", outline="black")  
            elif maze[y][x] == 123:
                canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, 
                                        fill="green", outline="black")
            else:
                canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, 
                                        fill="red", outline="black")
                canvas.create_text((x + 0.5) * cell_width, (y + 0.5) * cell_height, 
                                   text=str(maze[y][x]), fill="black", font=("Arial", 12), anchor=tk.CENTER)
    canvas.create_rectangle(start[0] * cell_width, start[1] * cell_height, (start[0] + 1) * cell_width, (start[1] + 1) * cell_height, 
                                        fill="orange", outline="black")

 

def draw_pi(pi):
    canvas_width = canvas.winfo_width()  
    canvas_height = canvas.winfo_height()
    # 计算每个单元格的尺寸（不包括padding）  
    cell_width = (canvas_width) // num_col
    cell_height = (canvas_height) // num_row
    global polies
    if len(polies):
        for id in polies:
            canvas.delete(id)
        polies = []
    
    for i,p in enumerate(pi):
        if maze[i//num_col][i%num_col] == 1:
            continue
        print(p)
        if  p[0] != 0:
            id = canvas.create_polygon((i%num_col+0.67)*cell_width,(i//num_col+0.33)*cell_height,
                       (i%num_col+0.67)*cell_width,(i//num_col+0.67)*cell_height,
                       (i%num_col+1)*cell_width,(i//num_col+0.5)*cell_height)
        if  p[1] != 0:
            id = canvas.create_polygon((i%num_col+0.33)*cell_width,(i//num_col+0.67)*cell_height,
                       (i%num_col+0.67)*cell_width,(i//num_col+0.67)*cell_height,
                       (i%num_col+0.5)*cell_width,(i//num_col+1)*cell_height)
        if  p[2] != 0:
            id = canvas.create_polygon((i%num_col+0.33)*cell_width,(i//num_col+0.33)*cell_height,
                       (i%num_col+0.33)*cell_width,(i//num_col+0.67)*cell_height,
                       (i%num_col)*cell_width,(i//num_col+0.5)*cell_height)
        if  p[3] != 0:
            id = canvas.create_polygon((i%num_col+0.33)*cell_width,(i//num_col+0.33)*cell_height,
                       (i%num_col+0.67)*cell_width,(i//num_col+0.33)*cell_height,
                       (i%num_col+0.5)*cell_width,(i//num_col)*cell_height)
        polies.append(id)           

def on_canvas_configure(event):  
    # 清除旧的网格  
    canvas.delete("all")  
    # 创建新的网格  
    draw_maze()
    if pi is not None:
        draw_pi(pi[:-1])

def component_replace():
    # 生成完地图后左边和下边的组件需重新grid
    canvas.grid(column=1, row=0, columnspan=num_col, rowspan=num_row, sticky=tk.W+tk.E+tk.N+tk.S)
    label1.grid(column=0, row=num_row+1, sticky='w', padx=10, pady=10)
    label2.grid(column=1, row=num_row+1, sticky='w', padx=10, pady=10)
    label3.grid(column=0, row=num_row+3, sticky='w', padx=10, pady=10)
    label4.grid(column=2, row=num_row+3, sticky='w', padx=10, pady=10)
    label5.grid(column=0, row=num_row+3, sticky='w', padx=10, pady=10)
    label6.grid(column=1, row=num_row+3, sticky='w', padx=10, pady=10)
    entry1.grid(column=0, row=num_row+2, padx=10, pady=10)
    entry2.grid(column=1, row=num_row+2, padx=10, pady=10)
    entrysx.grid(column=0, row=num_row+4, padx=10, pady=10)
    entrysy.grid(column=1, row=num_row+4, padx=10, pady=10)
    entryfx.grid(column=2, row=num_row+4, padx=10, pady=10)
    entryfy.grid(column=3, row=num_row+4, padx=10, pady=10)
    button_mix.grid(column=num_col+1,row=0, padx=10, pady=10, sticky=tk.W+tk.E)
    button_pi_iter.grid(column=num_col+1,row=1, padx=10, pady=10, sticky=tk.W+tk.E)
    button_value_iter.grid(column=num_col+1,row=2, padx=10, pady=10, sticky=tk.W+tk.E)
    button_sarsa.grid(column=num_col+1,row=3, padx=10, pady=10, sticky=tk.W+tk.E)
    map_button.grid(column=0, row=num_row+5, columnspan=1, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)
    uncertain_button.grid(column=1,row=num_row+5, columnspan=1,padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

    step_label.grid(column=num_col+1, row=num_row+2, padx=10, pady=10)

def get_entry():
    global end, start
    if entrysx.get() != "":
        start[0] = int(entrysx.get())
    if entrysy.get() != "":
        start[1] = int(entrysy.get())
    end = [num_col-1,num_row-1]
    if entryfx.get() != "":
        end[0] = int(entryfx.get())
    if entryfy.get() != "":
        end[1] = int(entryfy.get())

def start_end_valid():
    for i in [start[0],end[0]]:
        if i < 0 or i >= num_col:
            return False
    for j in [start[1],end[1]]:
        if j < 0 or j >= num_row:
            return False
    return True

def on_mapbutton_click():
    
    # 这里可以添加点击按钮后要在 Canvas 上执行的操作
    label_explain.grid_forget()
    if entry1.get() == "" or entry2.get() == "":
        messagebox.showwarning("提示","行数和列数不能为空！")
        return
    global num_col,num_row
    num_row = int(entry1.get())
    num_col = int(entry2.get())
    global mapready
    mapready = True
    
    get_entry()
    if not start_end_valid():
        messagebox.showwarning("提示","起点或终点输入有误！")
        return
    global maze
    maze = generate_pmap(num_col,num_row, 1000, *start, *end)
    maze = narrow3(maze, *start, *end)

    component_replace()

    draw_maze()

def uncertain_button_click():
    label_explain.grid_forget()
    if entry1.get() == "" or entry2.get() == "":
        messagebox.showwarning("提示","行数和列数不能为空！")
        return
    global num_col,num_row
    num_row = int(entry1.get())
    num_col = int(entry2.get())

    global mapready
    mapready = True

    get_entry()
    if not start_end_valid():
        messagebox.showwarning("提示","起点或终点输入有误！")
        return
    
    global maze
    maze = generate_pmap(num_col,num_row, 1000, *start, *end)
    maze = trap(maze,*start,*end)

    component_replace()

    draw_maze()

# 创建主窗口 
root = tk.Tk()  
root.title("首页")  
root.geometry("800x600")  # 设置窗口大小  
canvas = tk.Canvas(root, width=400, height=300)
root.configure(bg='black')

  
# 创建按钮，并设置其文本和命令  
button1 = tk.Button(root, text="深度优先", command=on_button1_click)
button2 = tk.Button(root, text="广度优先", command=on_button2_click)
button3 = tk.Button(root, text="一致代价", command=on_button3_click)  
button4 = tk.Button(root, text="贪心搜索", command=on_button4_click)
button5 = tk.Button(root, text="A*算法", command=on_button5_click)
button_pi_iter = tk.Button(root, text="策略迭代", command=on_button_pi_iter_click)
button_value_iter = tk.Button(root, text="价值迭代", command=on_button_value_iter_click)
button_sarsa = tk.Button(root, text="Sarsa算法", command=on_button_sarsa_click)

button_mix = tk.Button(root, text="对抗搜索", command=on_button_mix_click)
map_button = tk.Button(root, text="生成迷宫", command=on_mapbutton_click)
uncertain_button = tk.Button(root, text="生成不确定性搜索地图", command=uncertain_button_click)

# 列数文本框
entry1 = tk.Entry(root, width=30)  
entry1.grid(column=0, row=6, padx=10, pady=10)  
  
# 列数文本框  
entry2 = tk.Entry(root, width=30)  
entry2.grid(column=1, row=6, padx=10, pady=10)

# 起点横坐标文本框
entrysx = tk.Entry(root, width=30)  
entrysx.grid(column=0, row=8, padx=10, pady=10)  

# 起点纵坐标文本框  
entrysy = tk.Entry(root, width=30)  
entrysy.grid(column=1, row=8, padx=10, pady=10)

# 终点横坐标文本框
entryfx = tk.Entry(root, width=30)  
entryfx.grid(column=2, row=8, padx=10, pady=10)  

# 终点纵坐标文本框
entryfy = tk.Entry(root, width=30)  
entryfy.grid(column=3, row=8, padx=10, pady=10) 

label1 = tk.Label(root, text="请输入行数:")  
label1.grid(column=0, row=5, sticky='w', padx=10, pady=10)
label2 = tk.Label(root, text="请输入列数:")  
label2.grid(column=1, row=5, sticky='w', padx=10, pady=10)

label3 = tk.Label(root, text="请输入起点横坐标:")  
label3.grid(column=0, row=7, sticky='w', padx=10, pady=10)
label4 = tk.Label(root, text="请输入起点纵坐标:")  
label4.grid(column=2, row=7, sticky='w', padx=10, pady=10)

label5 = tk.Label(root, text="请输入终点横坐标:")  
label5.grid(column=2, row=7, sticky='w', padx=10, pady=10)
label6 = tk.Label(root, text="请输入终点纵坐标:")  
label6.grid(column=3, row=7, sticky='w', padx=10, pady=10)
label_explain = tk.Label(root, text="生成迷宫时请务必先输入行数、列数，\n 起点终点可以选择输入，\n默认为左上右下，\n生成用于策略迭代的地图时，\n 为方便起见，起点终点均为默认的左上和右下")  
label_explain.grid(column=3, row=0, rowspan=4,sticky=tk.W+tk.E+tk.N+tk.S)

step_label = tk.Label(root, text="花费的步数: ")
step_label.grid(column=2, row=6, padx=10, pady=10)

# 使用grid布局管理器放置按钮  
# 参数column和row指定按钮在网格中的位置，sticky参数用于设置按钮在其单元格内的对齐方式  
button1.grid(column=0, row=0, padx=10, pady=10, sticky=tk.W+tk.E)  # 水平居中  
button2.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W+tk.E)  # 水平居中
button3.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W+tk.E)  # 水平居中  
button4.grid(column=0, row=3, padx=10, pady=10, sticky=tk.W+tk.E)  # 水平居中
button5.grid(column=0, row=4, padx=10, pady=10, sticky=tk.W+tk.E)  # 水平居中 
button_mix.grid(column=2, row=0, padx=10, pady=10, sticky=tk.W+tk.E)  # 水平居中
button_pi_iter.grid(column=2, row=1, padx=10, pady=10, sticky=tk.W+tk.E)
button_value_iter.grid(column=2, row=2, padx=10, pady=10, sticky=tk.W+tk.E)
button_sarsa.grid(column=2, row=3, padx=10, pady=10, sticky=tk.W+tk.E)
uncertain_button.grid(column=1, row=9, columnspan=1, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)



map_button.grid(column=0, row=9, columnspan=1, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)  # 水平和垂直居中，并跨越两列  
  
# 配置列的权重，以便它们可以均匀扩展（如果需要的话）  
root.grid_columnconfigure(0, weight=1)  
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

root.grid_rowconfigure(0, weight=1)  
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)  
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)  
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)

canvas.bind("<Configure>", on_canvas_configure)
  
# 运行Tkinter的主循环  
root.mainloop()