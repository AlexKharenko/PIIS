import pygame
from player import Player
from ghost import Ghost
pygame.font.init()

class Game():
    def __init__(self):
        self.field_width = 800
        self.window_width = 600
        self.window_height = 720
        self.running = False
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.field_width, self.window_height))
        self.player = Player(30*5 +1,30*4+1,5)
        self.ghost = Ghost(31,31,5)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)

        pygame.display.set_caption("Pac Man")

    def start(self):
        self.running = True

    def drawScore(self):
        text = self.font.render('Score: '+str(self.player.score), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (700, 720//2)
        self.window.blit(text, textRect)

    def closeGame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   self.running = False

    def drawYouLose(self):
        text = self.font.render('You Lose!', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (700, 720//2)
        self.window.blit(text, textRect)
        self.window.fill((0,0,0))
        
            
    
    def checkLose(self):
        if self.player.x == self.ghost.x and self.player.y == self.ghost.y:
            self.player.direction = "stop"
            self.ghost.direction = "stop"
            self.running = False

    def checkWin(self, level):
        for i in range(len(level.matrix)):
            for j in range(len(level.matrix[i])):
                if level.matrix[i][j] == ".":
                    return 
        self.running = False

    def drawWindow(self, level):
        self.window.fill((0,0,0))
        level.drawMap(self.window)
        self.player.drawPlayer(self.window)
        self.ghost.drawGhost(self.window)
        self.drawScore()
        pygame.display.update()
