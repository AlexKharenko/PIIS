import pygame

class Char():
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.cell_w_h = 30
        

    def checkDirection(self, level, direction, window_height=None, window_width = None):
        if direction == "stop":
            return False
        if direction == None:
            return False
        i = (self.y - 1) // self.cell_w_h
        j = (self.x - 1) // self.cell_w_h

        if direction == "up":
            if self.y >= self.speed: 
                if level.matrix[i-1][j]!="=" or i==0:
                    if (self.x - 1) % self.cell_w_h != 0:
                        return False
                    return True
                elif self.y >= self.cell_w_h*i + self.speed + 1:
                    return True
                
        if direction == "down":
            if self.y < window_height - self.cell_w_h: 
                if level.matrix[i+1][j]!="=":
                    if (self.x - 1) % self.cell_w_h != 0:
                        return False
                    return True
        if direction == "left":
            if self.x >= self.speed: 
                if level.matrix[i][j-1]!="=" or j==0:
                    if (self.y - 1) % self.cell_w_h != 0:
                        return False
                    return True
                elif self.x>=self.cell_w_h*j + self.speed + 1:
                    return True
        if direction == "right":
            if self.x < window_width - self.cell_w_h: 
                if level.matrix[i][j+1]!="=":
                    if (self.y - 1) % self.cell_w_h != 0:
                        return False
                    return True
        return False
            
    def movePlayer(self, level, window_width, window_height):
        if self.checkDirection(level, self.direction, window_height, window_width) and not self.checkDirection(level, self.next_direction, window_height, window_width):
            if self.direction == "up":
                self.y-=self.speed
            elif self.direction == "down":
                self.y+=self.speed
            elif self.direction == "left":
                self.x-=self.speed
            elif self.direction == "right":
                self.x+=self.speed
        else:
            self.direction = "stop"
            if self.checkDirection(level, self.next_direction, window_height, window_width):
                self.direction = self.next_direction
                self.next_direction = None
        

   
    
    

