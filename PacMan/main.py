import pygame
import sys
sys.path.append("d:/Study/FiveSemester/PIIS/PacMan/libs")
# sys.setrecursionlimit(10000)

from game import Game
from level import Level
# from matrix import matrix
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
    game.botPlayer(algo, level)
    game.player.eatDot(level)
    for ghost in game.ghosts:
        game.botGhost(algo, level, ghost)
    
    game.drawWindow(level)

if game.win:
    game.drawWin()
if not game.win:
    game.drawYouLose()
pygame.time.delay(1000)






