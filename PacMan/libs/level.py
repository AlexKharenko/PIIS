import pygame
import random

class Level():
    def __init__(self, matrix = [[]]):
        self.width = 20
        self.height = 24
        self.matrix = matrix 
        self.max_dots = 400
        self.dots_count = self.width*self.height

    def randomWall(self):
        max_wall = 9
        min_wall = 1
        count_walls = random.randrange(min_wall, max_wall)
        ways = ['left', 'up', 'rigth', 'down']
        wall = []
        for counter in range(count_walls):
            wall.append(ways[random.randrange(0,3)])
        return wall
        
    def getSpawn(self):
        x = random.randrange(0, self.width-1)
        y = random.randrange(0, self.height-1)
        while self.matrix[y][x] != '.':
            x = random.randrange(0, self.width-1)
            y = random.randrange(0, self.height-1)
        return {'x': x, 'y':y}

    def levelGenerate(self):
        self.matrix = []
        for row in range(self.height):
            self.matrix.append(['.']*self.width)
        while self.max_dots < self.dots_count:
            # print(self.dots_count)
            x = random.randrange(0, self.width-1)
            y = random.randrange(0, self.height-1)
            # self.matrix[y][x] = "="

            wall = self.randomWall()
            for point in wall:
                if point == "left" and x > 0:
                    if self.matrix[y][x-1] == ".":
                        self.matrix[y][x-1] = "="
                        self.dots_count-=1
                if point == "right" and x < self.width-1:
                    if self.matrix[y][x+1] == ".":
                        self.matrix[y][x+1] = "="
                        self.dots_count-=1
                if point == "down" and y < self.height-1:
                    if self.matrix[y+1][x] == ".":
                        self.matrix[y+1][x] = "="
                        self.dots_count-=1
                if point == "up" and y > 0:
                    if self.matrix[y-1][x] == ".":
                        self.matrix[y-1][x] = "="
                        self.dots_count-=1

        
            


    def drawPath(self, screen, path, colour):
        for point in path:
            pygame.draw.rect(screen, colour, (point['x']*30+1, point['y']*30+1, 28, 28))

    def drawLevel(self, screen):
        wall_img = pygame.image.load('./assets/wall.png')
        dot_img = pygame.image.load('./assets/dot.png')
        if self.matrix != None:
            for i in range(self.height):
                for j in range(self.width):
                    if self.matrix[i][j] == "=":
                        screen.blit(wall_img, (30*j, 30*i))
                    if self.matrix[i][j] == ".":
                        screen.blit(dot_img, (30*j, 30*i))

    
