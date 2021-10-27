import pygame
import sys
import time
sys.path.append("d:/Study/FiveSemester/PIIS/PacMan/libs")
# sys.setrecursionlimit(10000)

from game import Game
from level import Level
# from matrix import matrix
from algo import Algorithm
from csw_writer import CSVWriter

game = Game()
game.start()

# level = Level(matrix)
level = Level()
level.levelGenerate()
game.setPlayerSpawn(level)
game.setGhostSpawn(level)
# level.setCharacters(game.player, game.ghosts)
algo = Algorithm(level)
tic = time.perf_counter()
while game.running:
    game.clock.tick(30)

    game.CheckEvents()
    keys = pygame.key.get_pressed()
    
    game.checkWin(level)
    if not game.running:
        continue
    game.checkLose()
    game.botPlayer(algo, level)
    game.player.eatDot(level)
    for i in range(game.ghosts_count):
        game.botGhost(algo, level, game.ghosts[i])
    for i in range(game.ghosts_random_count):
        game.ghosts[i+game.ghosts_count].movePlayer(level, game.window_width, game.window_height)
        game.ghosts[i+game.ghosts_count].choseDirection()   
    
    game.drawWindow(level)

toc = time.perf_counter()
algorithms = ['minimax','expectimax']
data = [False, f'{toc - tic:0.4f}', str(game.player.score), algorithms[1]]
csw = CSVWriter('./game.csv')
if game.win:
    game.drawYouWin()
    data[0]=True
if not game.win:
    game.drawYouLose()
csw.writeData(data)
pygame.time.delay(1000)






