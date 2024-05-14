"""AHHHHHHHHHHHHH"""
import os
import math
import random
import time

import pygame

from assets.scripts.particle import Particle
from assets.scripts.utils import darken
from assets.scripts.utils import get_angle


class Zombie:
    """I really don't know"""
    def __init__(self, display, fps, pos, player_rect, player_mask, player_pos, speed):
        """Zombie suc"""
        self.display = display
        self.FPS = fps
        self.dt = 1
        # Facing left
        self.dir = True
        # Animation
        path = os.path.join('images', 'zombie', 'zombie.png')
        path1 = os.path.join('images', 'zombie', 'zombie1.png')
        self.frames = [pygame.transform.scale_by(pygame.image.load(path), 2),
                       pygame.transform.scale_by(pygame.image.load(path1), 2)]
        self.frame = 0
        self.frame_count = 1
        self.frame_cap = self.FPS/4
        self.anim = True
        # Alpha
        self.alpha = 255
        self.alpha_change = 0
        # Zombie
        self.zombie = self.frames[self.frame]
        self.mask = pygame.mask.from_surface(self.zombie)
        self.player_mask = player_mask
        self.rect = self.frames[0].get_frect()
        self.pos = pygame.math.Vector2(pos)
        self.rect.center = self.pos
        self.speed = speed
        # Ded
        self.dead = False
        self.dead_time = time.time()
        self.kill = False
        self.kill_time = 0
        self.particles = []
        # Player
        self.player_pos = player_pos
        self.player_rect = player_rect
        self.player_health = 0
        self.bullets = []
        # hhah i hate this part

    def update(self):
        """Updates the zombie and stuff idk."""
        if self.dead and self.frame == 1:
            if int(time.time() - self.dead_time) + 3 * int(self.dead) <= self.kill_time * int(self.dead):
                self.alpha_change = -((int(time.time() - self.dead_time) + 3) * 60)/255
                self.alpha += self.alpha_change
                self.zombie.set_alpha(int(self.alpha))
        if not self.dead:
            self.player_collision()
            self.pos = pygame.math.Vector2(self.rect.center)
            angle = math.radians(get_angle(self.player_pos - self.pos))
            self.rect.centerx += math.cos(angle) * self.speed * self.dt
            self.rect.centery -= math.sin(angle) * self.speed * self.dt
        else:
            if int(time.time() - self.dead_time) >= self.kill_time:
                self.kill = True
        for particle in self.particles:
            particle.update()
            if particle.kill:
                self.particles.remove(particle)

    def animate(self):
        """Animates the zombie and stuff idk."""
        if self.anim:
            self.zombie = self.frames[self.frame]
            self.frame_count += 1
            if self.frame_count >= self.frame_cap:
                self.frame = 0 if self.frame == 1 else 1
                self.frame_count = 0
                self.zombie = self.frames[self.frame]
            if self.dead:
                if self.frame == 0 and self.frame_count + 1 >= self.frame_cap:
                    self.blood_particles()
                if self.frame + 1 == 2 and self.frame_count + 1 >= self.frame_cap:
                    self.anim = False
                    self.die()

    def player_collision(self):
        """checks for player and zombie collision and stuff idk."""
        if self.rect.colliderect(self.player_rect) and not self.dead:
            self.mask = pygame.mask.from_surface(self.zombie)
            if self.mask.overlap_mask(self.player_mask, self.player_rect.center):
                self.collision()
                self.player_health -= 1
        for bullet in self.bullets:
            if self.rect.colliderect(bullet.rect):
                self.collision()

    def collision(self):
        """Uh oh did i just run into a child crap."""
        self.dead = True
        self.dead_time = time.time()
        self.kill_time = random.randint(11, 17)  # seven is a
        self.frame = 0
        self.frame_cap = 5
        self.frame_count = 0
        self.frames = [pygame.transform.scale_by(pygame.image.load(r'images/zombie/dead1.png'), 2),
                       pygame.transform.scale_by(pygame.image.load(r'images/zombie/dead2.png'), 2)]

    def die(self):
        """Tysm."""
        self.zombie = pygame.image.load(r'images\zombie\blood' + str(random.randint(1, 2)) + '.png')
        self.pos = self.rect.center
        for i in range(random.randint(3, 5)):
            self.zombie.blit(darken(pygame.transform.scale_by(pygame.image.load(r'images/hero/blood_particle.png'), random.uniform(0.25, 0.5)), random.randint(25, 50)),
                             (random.randint(5, self.zombie.get_width()-5), random.randint(0, self.zombie.get_height()-5)))
        self.zombie = pygame.transform.scale_by(self.zombie, 1.5)
        self.rect = self.zombie.get_rect(center=self.pos)

    def blood_particles(self):
        """Yassssssssssssss."""
        self.particles = []
        self.particles = [
            Particle(self.display, r'\zombie\blood_particle.png', self.rect.center,
                     0.45 + random.uniform(-0.5, 0.5),
                     math.radians(get_angle(self.pos - pygame.math.Vector2(*pygame.mouse.get_pos())) +
                         random.randint(-90, -30) if random.randint(0, 1) else
                             random.randint(30, 90)),
                     0.45 + random.uniform(-0.5, 0.2)),

            Particle(self.display, r'\zombie\blood_particle.png', self.rect.center,
                     0.45 + random.uniform(-0.5, 0.5),
                     math.radians(get_angle(self.pos - pygame.math.Vector2(*pygame.mouse.get_pos())) +
                         random.randint(-90, -30) if random.randint(0, 1) else math.radians(
                             random.randint(30, 90))),
                     0.45 + random.uniform(-0.5, 0.2)),
            Particle(self.display, r'\zombie\blood_particle.png', self.rect.center,
                     0.45 + random.uniform(-0.5, 0.5),
                     math.radians(get_angle(self.pos - pygame.math.Vector2(*pygame.mouse.get_pos())) +
                         random.randint(-90, -30) if random.randint(0, 1) else
                             random.randint(30, 90)),
                     0.45 + random.uniform(-0.5, 0.2)),
            Particle(self.display, r'\zombie\blood_particle.png', self.rect.center,
                     0.45 + random.uniform(-0.5, 0.5),
                     math.radians(get_angle(self.pos - pygame.math.Vector2(*pygame.mouse.get_pos())) +
                                  random.randint(-90, -30) if random.randint(0, 1) else
                                  random.randint(30, 90)),
                     0.45 + random.uniform(-0.5, 0.2))
        ]

    def _face_player(self):
        """Baically what it sounds."""
        if self.rect.centerx < self.player_pos[0] and self.dir != True:
            self.frames[0] = pygame.transform.flip(self.frames[0], True, False)
            self.frames[1] = pygame.transform.flip(self.frames[1], True, False)
            self.dir = not self.dir
        elif self.rect.centerx > self.player_pos[0] and self.dir != False:
            self.frames[0] = pygame.transform.flip(self.frames[0], True, False)
            self.frames[1] = pygame.transform.flip(self.frames[1], True, False)
            self.dir = not self.dir

    def render(self):
        """Yeah you porbably know what this does."""
        self.animate()
        if not self.dead:
            self._face_player()
        self.display.blit(self.zombie, self.rect)
        for particle in self.particles:
            particle.render()
