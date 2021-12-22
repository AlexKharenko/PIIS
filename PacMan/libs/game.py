import pygame
import math
import time
from player import Player
from game_state import GameState
from ghost import Ghost
pygame.font.init()
from copy import deepcopy


class Game():
    def __init__(self):
        self.field_width = 800
        self.window_width = 300
        self.window_height = 300
        self.running = False
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(
            (self.field_width, self.window_height))
        self.player = ''
        self.ghosts_count = 0
        self.ghosts_random_count = 1
        self.ghosts = []
        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.algos = [{'name': 'bfs', 'colour': (204, 255, 255)}, {'name': 'dfs', 'colour': (
            255, 153, 204)}, {'name': 'ucs', 'colour': (204, 153, 255)}]
        self.colour = self.algos[0]['colour']
        self.current_algo = self.algos[0]['name']

        pygame.display.set_caption("Pac Man")

    def start(self):
        self.running = True

    def drawScore(self):
        text = self.font.render(
            'Score: '+str(self.player.score), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (700, self.window_height//2)
        self.window.blit(text, textRect)

    def CheckEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.changeAlgo()
        return False

    def drawYouLose(self):
        self.window.fill((0, 0, 0))
        text = self.font.render('You Lose!', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (800/2, self.window_height//2)
        self.window.blit(text, textRect)

        pygame.display.update()

    def drawYouWin(self):
        self.window.fill((0, 0, 0))
        text = self.font.render('You Win!', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (800/2, self.window_height//2)
        self.window.blit(text, textRect)

        pygame.display.update()

    def checkLose(self):
        for i in range(self.ghosts_count + self.ghosts_random_count):
            check = self.player.check_collision(self.ghosts[i])
            if check:
                self.player.direction = "stop"
                self.ghosts[i].direction = "stop"
                self.running = False

    def checkWin(self):
        if self.player.win:
            self.running = False

    def setPlayerSpawn(self, level, player=None):
        # point = level.getSpawn()
        if player == None:
            self.player = Player(30*4 + 1, 30*2+1, 5, level, self.window_width, self.window_height, {"width": len(level.matrix[0]),
                                                                                                     "height": len(level.matrix),
                                                                                                     "numTraining": 1000})
        else:
            self.player = player
            self.player.x = 30*4 + 1
            self.player.y = 30*2 + 1
            self.player.level = level

    def setGhostSpawn(self, level):
        for i in range(self.ghosts_count+self.ghosts_random_count):
            point = level.getSpawn()
            self.ghosts.append(Ghost(30*point['x'] + 1, 30*point['y']+1, 10))

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

    def updateCharCoords(self):
        self.player.updateCoordinates()
        for ghost in self.ghosts:
            ghost.updateCoordinates()

    def botPlayer(self, algo, level):
        point = self.player.goal_cor
        if self.player.goal_cor == None:
            self.player.goal_cor = level.getSpawn()
            point = self.player.goal_cor
        if level.matrix[point['y']][point['x']] == 2:
            self.player.goal_cor = level.getSpawn()
            point = self.player.goal_cor
        if (self.player.x-1) % 30 == 0 and (self.player.y-1) % 30 == 0:
            self.updateCharCoords()
            state = GameState(level.matrix)
            state.setPlayerAndGhostsCords(self.player, self.ghosts)
            self.player.root_node = algo.generateTree(
                state, (point['y'], point['x']))
            # best_value = algo.minimax(self.player.root_node, -math.inf, math.inf, 0)
            best_value = algo.expectimax(self.player.root_node, 0)
            (y, x) = self.findNewCoordsFromNodes(best_value)
            self.checkDirectionFromPath(self.player, [(x, y)])
        self.player.movePlayer(level, self.window_width, self.window_height)

    def findNewCoordsFromNodes(self, best_value):
        if len(self.player.root_node.children) == 0:
            return self.player.coord
        for child in self.player.root_node.children:
            if child.value == best_value:
                return child.state.player_coords

    def botGhost(self, algo, level, ghost):
        ghost.goal_cor = ((self.player.x-1)//30, (self.player.y-1)//30)
        if (ghost.x-1) % 30 == 0 and (ghost.y-1) % 30 == 0:
            self.updateCharCoords()
            self.useAlgo(algo, ((ghost.x-1)//30, (ghost.y-1)//30),
                         ghost.goal_cor)
            algo.restructPath()
            ghost.path = algo.path
            self.checkDirectionFromPath(ghost, ghost.path)
        ghost.movePlayer(level, self.window_width, self.window_height)

    def drawWindow(self, level):
        self.window.fill((0, 0, 0))
        level.drawLevel(self.window)
        self.player.drawPlayer(self.window)
        for ghost in self.ghosts:
            ghost.drawGhost(self.window)
        self.drawScore()
        pygame.display.update()
