import pygame
import sys
sys.path.append("d:/Study/FiveSemester/PIIS/PacMan/libs")
# sys.setrecursionlimit(10000)

from game import Game
from level import Level
from matrix import matrix
from algo import Algorithm

game = Game()
game.start()

# level = Level(matrix)
level = Level()
level.levelGenerate()
game.setPlayerSpawn(level)
game.setGhostSpawn(level)
algo = Algorithm(level)

while game.running:
    game.clock.tick(30)

    game.CheckEvents()
    keys = pygame.key.get_pressed()
    
    game.checkWin(level)
    game.checkLose()
    game.useAlgo(algo)
    game.player.movePlayer(level, game.window_width, game.window_height)
    game.ghost.movePlayer(level, game.window_width, game.window_height)
    game.player.eatDot(level)
    game.player.choseDirection(keys)
    game.ghost.choseDirection()

    game.drawWindow(level, algo.path)

if game.win:
    game.drawWin()
if not game.win:
    game.drawYouLose()
pygame.time.delay(1000)






