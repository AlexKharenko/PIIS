from char import Char
import pygame

class Player(Char):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.score = 0
        self.anim_counter = 0
        self.direction = "left"
        self.next_direction = None
        self.algo_colour = (204, 255, 204)
        self.stand_img = pygame.transform.scale(pygame.image.load('./assets/pacman/pac_stop.png'), (24,24))
        self.walk = {"right": [self.stand_img, pygame.transform.scale(pygame.image.load('./assets/pacman/pac_r1.png'), (24,24)),pygame.transform.scale(pygame.image.load('./assets/pacman/pac_r2.png'), (18,24)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_r1.png'), (24,24))],
            "left": [self.stand_img, pygame.transform.scale(pygame.image.load('./assets/pacman/pac_l1.png'), (24,24)),pygame.transform.scale(pygame.image.load('./assets/pacman/pac_l2.png'), (18,24)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_l1.png'), (24,24))],
            "up": [self.stand_img, pygame.transform.scale(pygame.image.load('./assets/pacman/pac_u1.png'), (24,24)),pygame.transform.scale(pygame.image.load('./assets/pacman/pac_u2.png'), (24,18)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_u1.png'), (24,24))],
            "down": [self.stand_img, pygame.transform.scale(pygame.image.load('./assets/pacman/pac_d1.png'), (24,24)),pygame.transform.scale(pygame.image.load('./assets/pacman/pac_d2.png'), (24,18)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_d1.png'), (24,24))],}

    
    def drawPlayer(self, screen):
        if self.anim_counter + 1 >= 20:
            self.anim_counter = 0
        if self.direction == "stop": 
            screen.blit(self.stand_img, (self.x+3,self.y+3))
            self.anim_counter = 0
        else:
            screen.blit(self.walk[self.direction][self.anim_counter // 5], (self.x+3,self.y+3))
            self.anim_counter += 1

    def eatDot(self, level):
        i = (self.y - 1) // self.cell_w_h
        j = (self.x - 1) // self.cell_w_h
        if level.matrix[i][j] == ".":
            level.matrix[i][j] = "_"
            self.score += 10


    def choseDirection(self, keys):
        if keys[pygame.K_LEFT]:
            self.next_direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.next_direction = "right"
        elif keys[pygame.K_UP]:
            self.next_direction = "up"
        elif keys[pygame.K_DOWN]:
            self.next_direction = "down"