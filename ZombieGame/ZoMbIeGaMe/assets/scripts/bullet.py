"""Bullet goes BRRRRRRRRRRRRRRRR"""
import pygame

from os import path

import pygame.math
import pygame.transform

class Bullet:
    """Basically it's a bullet that you shoot. Yeah, you're
    welcome. I'm so good at writing docstrings."""
    def __init__(self, display, pos, angle, speed, start_place, scale=1):
        """Initializes class."""
        # Display
        self.display = display
        # Pos, speed, angle
        self.pos = pos
        start_place_vec = pygame.math.Vector2()
        start_place_vec.from_polar((start_place, -angle))
        self.pos += start_place_vec
        self.speed = pygame.math.Vector2()
        self.speed.from_polar((speed, -angle))
        # Actual bullet and rect
        bullet = path.join(r'images', 'bullet', 'bullet.png')
        self.bullet = pygame.image.load(bullet).convert_alpha()
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.bullet = pygame.transform.scale_by(self.bullet, scale)
        self.rect = self.bullet.get_frect(center=pos)

    def update(self):
        """Moves the bullet."""
        self.pos += self.speed
        self.rect.center = self.pos

    def render(self):
        """Renders/draws the bullet/idk."""
        self.display.blit(self.bullet, self.rect)
