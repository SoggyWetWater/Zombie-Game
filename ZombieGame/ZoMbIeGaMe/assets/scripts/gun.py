"""I barely know how this works lol.... Yeah that's not good."""

import math
import time
from os import path
import random

import pygame

from assets.scripts.utils import rotate_on_pivot, get_angle_to_mouse
from assets.scripts.bullet import Bullet


class Gun:
    """Gun go pew pew and u go ded ded"""
    def __init__(self,  display, gun_num, pivot, offset, bullet_speed, fire_rate, cooldown, shot_amount, start_place):
        """Initialize stuff, what'd you think it did bro?"""
        self.display = display
        self.gun_num = gun_num
        gun = path.join('images', 'guns', f'gun{gun_num}.png')
        self.GUN_REF = pygame.image.load(gun).convert_alpha()
        self.GUN_REF = pygame.transform.scale_by(self.GUN_REF, 2)
        self.gun = self.GUN_REF
        self.gun_flipped = pygame.transform.flip(self.GUN_REF, False, True)
        self.rect = self.GUN_REF.get_frect()

        self.offset = pygame.math.Vector2(*offset)
        self.pivot = pivot
        self.pos = pivot + self.offset
        self.angle = get_angle_to_mouse(self.pos)

        self.bullets = []
        self.fire_rate = fire_rate # frfr no cap ongong crap why did i put this on gh
        self.wait_time = 0
        self.mouse_down = False
        self.bullet_speed = bullet_speed
        self.start_place = start_place
        self.shot_amount = shot_amount
        self.shots = self.shot_amount
        self.cooldown = cooldown
        self.cooldown_timer = time.time() # + self.cooldown
        # Yeah I hate it too
        self.SPEED = 2
        self.movement_x = 0
        self.movement_y = 0
        self.dt = 1

    def update(self, pos):
        """yeah, so actually this updates stuff."""
        self.pos = pos
        if self.movement_x != 0 and self.movement_y != 0:
            # man i hate normalizing vectors :(
            self.pos.x += math.sqrt(self.SPEED) * self.movement_x * self.dt
            self.pos.y += math.sqrt(self.SPEED) * self.movement_y * self.dt
        elif self.movement_x != 0:
            self.pos.x += self.SPEED * self.movement_x * self.dt
        elif self.movement_y != 0:
            self.pos.y += self.SPEED * self.movement_y * self.dt
        self.offset_pos = pos + self.offset
        self.angle = get_angle_to_mouse(self.pos)
        self.gun, self.rect = rotate_on_pivot(self.gun_flipped if pygame.mouse.get_pos()[0] < self.pos.x else self.GUN_REF, self.angle, self.pos, self.offset_pos)

        if self.mouse_down and self.wait_time - time.time() <= 0 and self.cooldown_timer - time.time() <= 0:
            self.shoot()
            self.wait_time = time.time() + self.fire_rate
            if self.shots - 1 <= 0:
                self.shots = self.shot_amount
                self.cooldown_timer = time.time() + self.cooldown

    def render(self):
        """Omgoodness, this renders/draws/blits/idktheflippingtechnicaltermorcarehahayoureadallofthisl stuff?"""
        self.display.blit(self.gun, self.rect)

    # Bullet stuff
    def shoot(self):
        """Yep, this is what shooting is like."""
        # i'm aware, it's a choice
        if self.gun_num == 2:
            angle = self.angle - 10
            for i in range(0, 20, 2):
                self.bullets.append(
                    Bullet(self.display, pygame.math.Vector2(self.rect.center), angle + i,
                           self.bullet_speed, self.start_place))
        else:
            self.bullets.append(
                Bullet(self.display, pygame.math.Vector2(self.rect.center), self.angle, self.bullet_speed, self.start_place))
        self.shots -= 1

    def update_bullets(self):
        """Yep, this updates bullets."""  # I only wrote the Y and it suggested the rect soo, good on you jetbrains
        # Bullets
        for bullet in self.bullets:
            bullet.update()
            if not bullet.rect.colliderect(self.display.get_rect()):
                self.bullets.remove(bullet)
                del bullet

    def render_bullets(self):
        """It renders things bro. That's crazy. LIkE uR MoM."""
        for bullet in self.bullets:
            bullet.render()
