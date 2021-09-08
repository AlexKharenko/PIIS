import pygame

class Map():
    def __init__(self, matrix):
        self.width = 20
        self.height = 24
        self.matrix = matrix

    def drawMap(self, screen):
        wall_img = pygame.image.load('./assets/wall.png')
        dot_img = pygame.image.load('./assets/dot.png')
        if self.matrix != None:
            for i in range(self.height):
                for j in range(self.width):
                    if self.matrix[i][j] == "=":
                        screen.blit(wall_img, (30*j, 30*i))
                    if self.matrix[i][j] == ".":
                        screen.blit(dot_img, (30*j, 30*i))

    
