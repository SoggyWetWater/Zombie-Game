"""You. This. Is. YOu. Loser hahahaahhaaa oh make it stop please"""
import math
import time
from math import floor
from random import randint
# TO DO MAKE BULLET CARRY PLAYER speed
# ADD DELTA MOVEMENT STUFF

import pygame

from assets.scripts.gun import Gun
from assets.scripts.utils import sprite_info
from assets.scripts.utils import change_hue, darken, get_angle_to_mouse


class Player:
    """This u, and just like ur mom i never want to make it again. haha u thought i lov u"""
    def __init__(self, display, fps):
        """This also u getting initialized."""
        self.display = display
        self.display_rect = self.display.get_rect()
        # change file numbering and delete + 1 add the end
        self.facing_left = True
        self.FPS = fps
        self.dt = 0
        self.frame = 0
        self.head_num = randint(1, 17)
        self.frames = self.get_frames(self.head_num)
        self.frame_count = 1
        self.frame_cap = 20
        self.speed = 2
        self.movement_x = 0
        self.movement_y = 0
        self.player = self.frames[self.frame]
        self.mask = pygame.mask.from_surface(self.player)
        self.rect = self.frames[0].get_frect()
        self.pos = pygame.math.Vector2(self.display_rect.width/2, self.display_rect.height/2)
        self.rect.center = self.pos
        # Player
        self.health = 5
        self.gun_num = 1                                                                    # That \/ number was very delibrate
        self.guns = {1: Gun(self.display, 1, pygame.math.Vector2(*self.rect.center), (25, 0), 14, 0.85, 0, 0,0),
                     2: Gun(self.display, 2, pygame.math.Vector2(*self.rect.center), (40, 0), 26, 1.45, 45, 8, 6),
                     3: Gun(self.display, 3, pygame.math.Vector2(*self.rect.center), (45, 0), 20, 0.35, 85, 245, 10),
                     4: Gun(self.display, 4, pygame.math.Vector2(*self.rect.center), (50, 0), 28, 0, 180, 300,10),
                     5: Gun(self.display, 5, pygame.math.Vector2(*self.rect.center), (55, 0), 999*999, 999*999, 999*999, 0, -12),
                     6: Gun(self.display, 6, pygame.math.Vector2(*self.rect.center), (45, 0), 999*999, 999*999, 999*999, 0, -24),
                     }
        self.gun = self.guns[self.gun_num]
        self.angle = get_angle_to_mouse(self.pos)
        self.off_screen_time = 0

    def update(self):
        """This update player"""
        self.mask = pygame.mask.from_surface(self.player)
        self.gun = self.guns[self.gun_num]
        self.pos = pygame.math.Vector2(self.rect.center)
        self.angle = int(get_angle_to_mouse(self.pos))
        if self.movement_x != 0 and self.movement_y != 0:
            # man i hate normalizing vectors :(
            self.rect.centerx += math.sqrt(self.speed) * self.movement_x * self.dt
            self.rect.centery += math.sqrt(self.speed) * self.movement_y * self.dt
        elif self.movement_x != 0:
            self.rect.centerx += self.speed * self.movement_x * self.dt
        elif self.movement_y != 0:
            self.rect.centery += self.speed * self.movement_y * self.dt
        if self.movement_x != 0 or self.movement_y != 0:
            self.frame_count += 1
            if self.frame_count >= self.frame_cap + 1:
                self.frame_count = 1
                self.frame = int(not self.frame)
        on_screen = self.rect.colliderect(self.display_rect)
        if not on_screen:
            if self.off_screen_time == 0:
                self.off_screen_time = time.time() + 3.5
            else:
                if self.off_screen_time <= time.time():
                    self.health = 0
        else:
            self.off_screen_time = 0

    def animate(self):
        """"Get animated nerd, yeah nerd isn't  an insult."""
        self.update() # As far as you're concerned, this doesn't exist.
        self.player = self.frames[self.frame]

    def _change_facing_direction(self, facing_left):
        """Just face in the direction."""
        if self.facing_left != facing_left:
            self.facing_left = not self.facing_left
            self.frames[0] = pygame.transform.flip(self.frames[0], True, False)
            self.frames[1] = pygame.transform.flip(self.frames[1], True, False)
            self.player = self.frames[self.frame]
            if self.head_num != 4 and self.head_num != 6:
                self.rect.centerx += self.rect.width - 32.02 if self.facing_left else 32.02 - self.rect.width
            elif self.head_num == 6:
                self.rect.centerx += -2 if self.facing_left else 2

    def render(self):
        """You know what this does."""
        self.animate()
        # hah you think rotating things is easy  i spent 3 hours on this so you're freaking wrong :)
        if self.rect.centerx < pygame.mouse.get_pos()[0]:
            self._change_facing_direction(True)
        if self.rect.centerx > pygame.mouse.get_pos()[0]:
            self._change_facing_direction(False)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.display.blit(self.player, self.pos)

    def get_frames(self, head_num):
        """AHhhhhhhhhhhh this i hate this it suck.
        I mean, would you rather i not write docstrings?"""
        hue = randint(0, 140)
        bottom = pygame.image.load(r'images\hero\bottom\bottom0.png').convert_alpha()
        bottom1 = pygame.image.load(r'images\hero\bottom\bottom1.png').convert_alpha()
        bottom = change_hue(bottom, hue)
        bottom1 = change_hue(bottom1, hue)
        top = pygame.image.load(r'images\hero\top\top' + str(head_num + 1) + '.png').convert_alpha()
        SPRITE_INFO = sprite_info[head_num]
        player = pygame.Surface((SPRITE_INFO['size']), pygame.SRCALPHA)
        player1 = player.copy()
        player.blit(bottom, (SPRITE_INFO['pos0']))
        player.blit(top, (SPRITE_INFO['top_pos']))
        player = pygame.transform.scale_by(player, 2)
        player1.blit(bottom1, (SPRITE_INFO['pos0'][0]+0, SPRITE_INFO['pos0'][1]-2))
        player1.blit(top, (0, 0))
        player1 = pygame.transform.scale_by(player1, 2)

        number = randint(1, 25)
        return [darken(player.copy(), number), darken(player1.copy(), number)]
