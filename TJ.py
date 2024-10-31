CELL_SIZE = 20

class Jerry:
    
    def __init__(self,x,y,color='red'):
        self.x = x
        self.y = y
        self.id = None
        self.color = color

    def can_move(self,move,maze):
        x = self.x + move[1]
        y = self.y + move[0]
        return x >= 0 and x <= maze.shape[1]\
            and y >= 0 and y <= maze.shape[0]\
            and maze[y][x] != 1
    
    def move(self,move):
        self.x = self.x + move[1]
        self.y = self.y + move[0]
    
    def update(self,canvas):
        if self.id is not None:
            canvas.delete(self.id)
        self.id = canvas.create_oval(self.x * CELL_SIZE + CELL_SIZE // 4, self.y * CELL_SIZE + CELL_SIZE // 4,  
                        (self.x + 1) * CELL_SIZE - CELL_SIZE // 4, (self.y + 1) * CELL_SIZE - CELL_SIZE // 4, fill=self.color)
        


        