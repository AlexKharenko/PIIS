from csw_writer import CSVWriter
from algo import Algorithm
from level import Level
from game import Game
import pygame
import sys
import time
sys.path.append("d:/Study/FiveSemester/PIIS/PacMan/libs")
# sys.setrecursionlimit(10000)


def game(matrix, pacman):
    game = Game()
    game.start()
    toQuit = False
    level = Level(matrix)
    # level = Level()
    # level.levelGenerate()
    game.setPlayerSpawn(level,pacman)
    game.setGhostSpawn(level)
    # level.setCharacters(game.player, game.ghosts)
    algo = Algorithm(level)
    while game.running:
        game.clock.tick(120)

        if game.CheckEvents():
            toQuit=True
        # keys = pygame.key.get_pressed()

        game.checkWin()
        if not game.running:
            game.player.score += 50
            game.player.observation_step(final=True)
            break
        game.checkLose()
        if not game.running:
            game.player.score -= 10
            game.player.observation_step(final=True)
            break
        game.player.ai_move()
        game.player.eatDot(level)
        for i in range(game.ghosts_count):
            game.botGhost(algo, level, game.ghosts[i])
        for i in range(game.ghosts_random_count):
            game.ghosts[i+game.ghosts_count].movePlayer(
                level, game.window_width, game.window_height)
            game.ghosts[i+game.ghosts_count].choseDirection()

        game.drawWindow(level)
    global last_game_result
    last_game_result = (game.player.score, game.player.win)
    return toQuit, last_game_result, game.player

# toc = time.perf_counter()
# algorithms = ['minimax','expectimax']
# data = [False, f'{toc - tic:0.4f}', str(game.player.score), algorithms[1]]
# csw = CSVWriter('./game.csv')
# if game.win:
#     game.drawYouWin()
#     data[0]=True
# if not game.win:
#     game.drawYouLose()
# csw.writeData(data)
# pygame.time.delay(1000)
