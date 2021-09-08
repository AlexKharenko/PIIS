import pygame

class Wall():
    def __init__(self, x, y):
        self.wall_img = pygame.image.load('./assets/wall.png')
        self.x = x
        self.y = y

    def drawWall(self, screen):
        screen.blit(self.wall_img, (self.x, self.y))
        # pygame.draw.rect(screen, (255,0,0), (self.x,self.y,self.width, self.height))