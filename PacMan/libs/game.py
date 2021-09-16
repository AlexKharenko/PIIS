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
        self.player = ''
        self.ghosts_count = 4
        self.ghosts = []
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.algos = [{'name': 'bfs', 'colour':(204, 255, 255)},{'name': 'dfs', 'colour':(255, 153, 204)},{'name': 'ucs', 'colour':(204, 153, 255)}]
        self.colour = self.algos[0]['colour']
        self.current_algo = self.algos[0]['name']
        self.win = False

        pygame.display.set_caption("Pac Man")


    def start(self):
        self.running = True

    def drawScore(self):
        text = self.font.render('Score: '+str(self.player.score), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (700, 720//2)
        self.window.blit(text, textRect)

    def CheckEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                   self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.changeAlgo()

    def drawYouLose(self):
        self.window.fill((0,0,0))
        text = self.font.render('You Lose!', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (800/2, 720//2)
        self.window.blit(text, textRect)
        
        pygame.display.update()

    def drawYouWin(self):
        self.window.fill((0,0,0))
        text = self.font.render('You Win!', True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (800/2, 720//2)
        self.window.blit(text, textRect)
        
        pygame.display.update()
        
    def checkLose(self):
        for i in range(self.ghosts_count):
            if self.player.x == self.ghosts[i].x and self.player.y == self.ghosts[i].y:
                self.player.direction = "stop"
                self.ghosts[i].direction = "stop"
                self.running = False

    def checkWin(self, level):
        for i in range(len(level.matrix)):
            for j in range(len(level.matrix[i])):
                if level.matrix[i][j] == ".":
                    return 
        self.running = False
        self.win = True

    def setPlayerSpawn(self, level):
        point = level.getSpawn()
        self.player = Player(30*point['x'] +1,30*point['y']+1,5)
        
        
    def setGhostSpawn(self, level):
        for i in range(self.ghosts_count):
            point = level.getSpawn()
            self.ghosts.append(Ghost(30*point['x'] +1,30*point['y']+1,5))

    def changeAlgo(self):
        if self.current_algo == self.algos[0]['name']:
            self.current_algo = self.algos[1]['name']
            self.colour = self.algos[1]['colour']
        elif self.current_algo == self.algos[1]['name']:
            self.current_algo = self.algos[2]['name']
            self.colour = self.algos[2]['colour']
        elif self.current_algo == self.algos[2]['name']:
            self.current_algo = self.algos[0]['name']
            self.colour = self.algos[0]['colour']

    def useAlgo(self, algo):
        player_cord = {'x': (self.player.x-1)//30, 'y': (self.player.y-1)//30}
        ghost_cord = {'x': (self.ghosts[0].x-1)//30, 'y': (self.ghosts[0].y-1)//30}
        if self.current_algo == 'bfs':
            algo.bfs(player_cord, ghost_cord)
        if self.current_algo == 'dfs':
            algo.dfs(player_cord, ghost_cord)
        if self.current_algo == 'ucs':
            algo.ucs(player_cord, ghost_cord)

    def drawWindow(self, level, path):
        self.window.fill((0,0,0))
        level.drawPath(self.window, path, self.colour)
        level.drawLevel(self.window)
        self.player.drawPlayer(self.window)
        for i in range(self.ghosts_count):
            self.ghosts[i].drawGhost(self.window)
        self.drawScore()
        pygame.display.update()
