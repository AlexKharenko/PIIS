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

    def useAlgo(self, algo, ghost_cord, player_cord):
        player_cord = {'x': player_cord[0], 'y': player_cord[1]}
        ghost_cord = {'x': ghost_cord[0], 'y': ghost_cord[1]}
        if self.current_algo == 'bfs':
            algo.bfs(ghost_cord, player_cord)
        if self.current_algo == 'dfs':
            algo.dfs(ghost_cord, player_cord)
        if self.current_algo == 'ucs':
            algo.ucs(ghost_cord, player_cord)

    def checkDirectionFromPath(self, char, path):
        if path == None or path == []:
            char.direction = "stop"
            return 
        if (char.x-1)//30 - path[0][0] == 1:
            char.direction = "left"
            return 
        elif (char.x-1)//30 - path[0][0] == -1:
            char.direction = "right"
            return 
        elif (char.y-1)//30 - path[0][1] == 1:
            char.direction = "up"
            return 
        elif (char.y-1)//30 - path[0][1] == -1:
            char.direction = "down"
            return 

    def botPlayer(self, algo, level):
        point = self.player.goal_cor
        if self.player.goal_cor == None:
            self.player.goal_cor = level.getSpawn()
            point = self.player.goal_cor
        if level.matrix[point['y']][point['x']] == "_":
            self.player.goal_cor = level.getSpawn()
            point = self.player.goal_cor
        if (self.player.x-1)%30 == 0 and (self.player.y-1)%30 == 0:
            algo.astar_search(((self.player.x-1)//30, (self.player.y-1)//30), (point['x'], point['y']))
            self.player.path = algo.path
        self.checkDirectionFromPath(self.player, self.player.path)
        self.player.movePlayer(level, self.window_width, self.window_height)

    def botGhost(self, algo, level, ghost):
        ghost.goal_cor = ((self.player.x-1)//30, (self.player.y-1)//30)
        if (ghost.x-1)%30 == 0 and (ghost.y-1)%30 == 0:
            self.useAlgo(algo, ((ghost.x-1)//30, (ghost.y-1)//30), ghost.goal_cor)
            algo.restructPath()
            ghost.path = algo.path
        self.checkDirectionFromPath(ghost, ghost.path)
        ghost.movePlayer(level, self.window_width, self.window_height)


    def drawWindow(self, level):
        self.window.fill((0,0,0))
        level.drawPath(self.window, self.player.path, self.player.algo_colour)
        # for ghost in self.ghosts:
        #     level.drawPath(self.window, ghost.path, self.colour)
        level.drawLevel(self.window)
        self.player.drawPlayer(self.window)
        for ghost in self.ghosts:
            ghost.drawGhost(self.window)
        self.drawScore()
        pygame.display.update()
