from char import Char
import pygame
import random


class Ghost(Char):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.anim_counter = 0
        self.direction_count = 0
        self.direction = "left"
        self.next_direction = None
        self.walk = {"right":pygame.transform.scale(pygame.image.load('./assets/ghosts/red_r.png'), (22,22)),
            "left": pygame.transform.scale(pygame.image.load('./assets/ghosts/red_l.png'), (22,22)),
            "up": pygame.transform.scale(pygame.image.load('./assets/ghosts/red_u.png'), (22,22)),
            "down": pygame.transform.scale(pygame.image.load('./assets/ghosts/red_d.png'), (22,22)),
            "stop": pygame.transform.scale(pygame.image.load('./assets/ghosts/red_stop.png'), (22,22)),
            "anim_array": [2,3,4,5,6,5,4,3,2]}

    
    def drawGhost(self, screen):
        if self.anim_counter < len(self.walk["anim_array"]):
            screen.blit(self.walk[self.direction], (self.x+4,self.y+self.walk["anim_array"][self.anim_counter]))
            self.anim_counter += 1
        else:
            self.anim_counter = 0


    def choseDirection(self):
        if self.direction_count <=30:
            self.direction_count += 1
        else:
            ways = ["left", "up", "right", "down"]
            self.next_direction = ways[random.randrange(5)-1]
            self.direction_count = 0
        