import pygame
import sys
sys.path.append("d:/Study/FiveSemester/PIIS/PacMan/libs")

from game import Game
from map_class import Map
from level import matrix

game = Game()
game.start()

level = Map(matrix)

while game.running:
    game.clock.tick(30)

    game.closeGame()
    keys = pygame.key.get_pressed()

    game.checkWin(level)
    game.checkLose()
    game.player.movePlayer(level, game.window_width, game.window_height)
    game.ghost.movePlayer(level, game.window_width, game.window_height)
    game.player.eatDot(level)
    game.player.choseDirection(keys)
    game.ghost.choseDirection()

    game.drawWindow(level)





