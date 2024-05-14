"""Yeah... I know"""
import math
import random
import time

import pygame


class Particle:
    def __init__(self, display, image, pos, speed, angle, kill_time, size=False):  # Yeah that's what she said
        self.display = display
        self.kill = False
        self.kill_time = time.time() + kill_time
        self.start_time = time.time()
        self.pos = list(pos)
        self.image = pygame.image.load(f'images\{image}')
        if size:
            self.image = pygame.transform.scale_by(self.image, 1.2 + random.uniform(-0.15, 0.35))
        self.rect = self.image.get_frect(center=pos)
        self.speed = speed
        self.d_alpha = 255
        self.angle = angle
        run_time = (self.kill_time - time.time()) * 60
        self.alpha_change = self.alpha_change = -(255/((run_time)))

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] -= math.sin(self.angle) * self.speed
        if time.time() - self.start_time >= self.kill_time:
            self.kill = True
        self.rect.center = self.pos
        self.d_alpha += self.alpha_change
        self.image.set_alpha(int(self.d_alpha))
        if self.kill_time <= time.time():
            self.kill = True

    def render(self):
        self.display.blit(self.image, self.rect.center)
