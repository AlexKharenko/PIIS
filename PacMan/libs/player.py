from char import Char
import pygame

import numpy as np
import random
from time import time, strftime, localtime
import sys


# Replay memory
from collections import deque

# Neural nets
import tensorflow as tf
from DQN import *

params = {
    "width": 10,
    "height": 10,
    "num_training": 10000,
    # Model backups
    'load_file': None,
    'save_file': None,
    'save_interval': 20,

    # Training parameters
    'train_start': 30,    # Episodes before training starts
    'batch_size': 32,       # Replay memory batch size
    'mem_size': 100000,     # Replay memory size

    'discount': 0.95,       # Discount rate (gamma value)
    'lr': .0002,            # Learning reate
    # 'rms_decay': 0.99,      # RMS Prop decay (switched to adam)
    # 'rms_eps': 1e-6,        # RMS Prop epsilon (switched to adam)

    # Epsilon value (epsilon-greedy)
    'eps': 1.0,             # Epsilon start value
    'eps_final': 0.1,       # Epsilon end value
    'eps_step': 10000       # Epsilon steps between start and end (linear)
}

qnet = DQN(params)


class Player(Char):
    def __init__(self, x, y, speed, level, w_w, w_h, args):
        super().__init__(x, y, speed)
        self.score = 0
        self.win = False
        self.level = level
        self.w_w = w_w
        self.w_h = w_h
        self.anim_counter = 0
        self.direction = "stop"
        self.root_node = None
        self.next_direction = None
        self.last_action = None
        self.terminal = True
        self.ep_rew = 0
        self.debounceCounter = 0
        self.algo_colour = (204, 255, 204)
        self.stand_img = pygame.transform.scale(
            pygame.image.load('./assets/pacman/pac_stop.png'), (24, 24))
        self.walk = {"right": [self.stand_img, pygame.transform.scale(pygame.image.load('./assets/pacman/pac_r1.png'), (24, 24)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_r2.png'), (18, 24)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_r1.png'), (24, 24))],
                     "left": [self.stand_img, pygame.transform.scale(pygame.image.load('./assets/pacman/pac_l1.png'), (24, 24)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_l2.png'), (18, 24)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_l1.png'), (24, 24))],
                     "up": [self.stand_img, pygame.transform.scale(pygame.image.load('./assets/pacman/pac_u1.png'), (24, 24)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_u2.png'), (24, 18)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_u1.png'), (24, 24))],
                     "down": [self.stand_img, pygame.transform.scale(pygame.image.load('./assets/pacman/pac_d1.png'), (24, 24)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_d2.png'), (24, 18)), pygame.transform.scale(pygame.image.load('./assets/pacman/pac_d1.png'), (24, 24))], }
        self.params = params
        gpu_options = tf.compat.v1.GPUOptions(
            per_process_gpu_memory_fraction=0.1)
        self.sess = tf.compat.v1.Session(
            config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
        self.qnet = qnet

        self.general_record_time = strftime(
            "%a_%d_%b_%Y_%H_%M_%S", localtime())

        self.Q_global = []
        self.cost_disp = 0

        self.cnt = self.qnet.sess.run(self.qnet.global_step)
        self.local_cnt = 0

        self.numeps = 0
        self.last_score = 0
        self.s = time()
        self.last_reward = 0.

        self.replay_mem = deque()
        self.last_scores = deque()

    def reset(self):
        self.win = False
        self.numeps += 1
        self.last_action = None
        self.anim_counter = 0
        self.terminal = True
        self.ep_rew = 0
        self.debounceCounter = 0
        self.Q_global = []
        self.cost_disp = 0

        # Stats
        self.cnt = self.qnet.sess.run(self.qnet.global_step)
        self.local_cnt = 0

        self.last_score = 0
        self.s = time()
        self.last_reward = 0.

        self.replay_mem = deque()
        self.last_scores = deque()

        self.score = 0

    def ai_move(self):
        self.debounceCounter += 1

        if (self.x-1) % 30 == 0 and (self.y-1) % 30 == 0:
            # print(self.debounceCounter)
            if self.debounceCounter >= 20:
                self.debounceCounter = 0
                self.observation_step()
            r = np.random.rand()
            # print(r, self.params['eps'], r > self.params['eps'])
            if r > self.params['eps']:
                self.Q_pred = self.qnet.sess.run(
                    self.qnet.y,
                    feed_dict={self.qnet.x: np.reshape(self.level.matrix,
                                                       (1, self.params['width'], self.params['height'], 1)),
                               self.qnet.q_t: np.zeros(1),
                               self.qnet.actions: np.zeros((1, 4)),
                               self.qnet.terminals: np.zeros(1),
                               self.qnet.rewards: np.zeros(1)})[0]

                self.Q_global.append(max(self.Q_pred))
                print(self.Q_pred)
                a_winner = np.argwhere(self.Q_pred == np.amax(self.Q_pred))
                print(a_winner)
                if len(a_winner) > 1:
                    move = a_winner[np.random.randint(0, len(a_winner))][0]
                else:
                    move = a_winner[0][0]
            else:
                move = np.random.randint(0, 4)

            self.change_direction(move)
            self.last_action = move

        self.move()

    def change_direction(self, value):
        if value == 0.:
            self.direction = "up"
        elif value == 1.:
            self.direction = "right"
        elif value == 2.:
            self.direction = "down"
        else:
            self.direction = "left"

    def train(self):
        # Train
        if (self.local_cnt > self.params['train_start']):
            batch = random.sample(self.replay_mem, self.params['batch_size'])
            batch_s = []  # States (s)
            batch_r = []  # Rewards (r)
            batch_a = []  # Actions (a)
            batch_n = []  # Next states (s')
            batch_t = []  # Terminal state (t)

            for i in batch:
                batch_s.append(i[0])
                batch_r.append(i[1])
                batch_a.append(i[2])
                batch_n.append(np.transpose(i[3]))
                batch_t.append(i[4])
            batch_s = np.reshape(
                batch_s[0], (1, self.params['width'], self.params['height'], 1))
            batch_r = np.array(batch_r)
            batch_a = self.get_onehot(np.array(batch_a))
            batch_n = np.reshape(
                batch_n[0], (1, self.params['width'], self.params['height'], 1))
            batch_t = np.array(batch_t)

            self.cnt, self.cost_disp = self.qnet.train(
                batch_s, batch_a, batch_t, batch_n, batch_r)

    def get_onehot(self, actions):
        """ Create list of vectors with 1 values at index of action in list """
        actions_onehot = np.zeros((self.params['batch_size'], 4))
        for i in range(len(actions)):
            actions_onehot[i][int(actions[i])] = 1
        return actions_onehot

    def observation_step(self, final=False):
        if self.last_action is not None:
            self.last_state = np.copy(self.level.matrix)

            # Process current experience reward
            self.current_score = self.score
            reward = self.current_score - self.last_score
            self.last_score = self.current_score
            
            if reward >= 50:
                self.last_reward = 400
            elif reward >= 10:
                self.last_reward = 70
            elif reward <= -10:
                self.last_reward = -1000
            elif reward <= 0:
                self.last_reward = -8

            self.ep_rew += self.last_reward

            experience = (self.last_state, float(self.last_reward),
                          self.last_action, self.level.matrix, self.terminal)
            self.replay_mem.append(experience)
            if len(self.replay_mem) > self.params['mem_size']:
                self.replay_mem.popleft()

            if final and params['save_file']:
                # and self.local_cnt % self.params['save_interval'] == 0:
                if self.local_cnt > self.params['train_start']:
                    print("save")
                    self.qnet.save_ckpt(
                        './saves/model-' + params['save_file'] + "_" + str(self.cnt) + '_' + str(self.numeps))

            self.train()

        self.local_cnt += 1
        self.anim_counter += 1
        self.params['eps'] = max(self.params['eps_final'],
                                 1.00 - float(self.cnt) / float(self.params['eps_step']))

    def check_for_empty_matrix(self, matrix):
        for line in matrix:
            for num in line:
                if num == 1:
                    return False
        return True

    def move(self):
        if (self.x-1) % 30 == 0 and (self.y-1) % 30 == 0:
            self.eatDot(self.level)
            empty = self.check_for_empty_matrix(self.level.matrix)
            if empty:
                self.win = True
                return

        self.movePlayer(self.level, self.w_w, self.w_h)

    def drawPlayer(self, screen):
        if self.anim_counter + 1 >= 20:
            self.anim_counter = 0
        if self.direction == "stop":
            screen.blit(self.stand_img, (self.x+3, self.y+3))
            self.anim_counter = 0
        else:
            screen.blit(self.walk[self.direction]
                        [self.anim_counter // 5], (self.x+3, self.y+3))
            self.anim_counter += 1

    def eatDot(self, level):
        i = (self.y - 1) // self.cell_w_h
        j = (self.x - 1) // self.cell_w_h
        if level.matrix[i][j] == 1:
            level.matrix[i][j] = 2
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
