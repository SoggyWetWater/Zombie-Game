""""NOAH ADD SOUNNNNNNNNNNNNNNNNNNNDS NOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"""

import sys
import json
import math # ye def high
import random
import time

import pygame
from pygame import mouse

from assets.scripts.player import Player
from assets.scripts.zombie import Zombie
from assets.scripts.hud import HUD
from assets.scripts.utils import keys
from assets.scripts.medkit import MedKit
from assets.scripts.particle import Particle
from assets.scripts.text import Text

pygame.init()


class ZombieGame:
    """Handles the game stuff."""
    # Yes ofc i know not to put that in init. Uhhhhhh actually wgjadfklajf nvm
    GAME_WIDTH = 480
    GAME_HEIGHT = 360
    TARGET_FPS = 60

    def __init__(self):
        """Uh this initializes stuff."""
        # Window setup
        sizes = pygame.display.get_desktop_sizes()
        game_scale = sizes[0][1] // self.GAME_HEIGHT
        window_width = game_scale * self.GAME_WIDTH
        window_height = game_scale * self.GAME_HEIGHT
        self.display = pygame.display.set_mode((window_width, window_height))
        caption = "ZoMbIe GaMe"
        pygame.display.set_caption(caption)
        icon = pygame.image.load(r"images\general\icon.png").convert()
        pygame.display.set_icon(icon)
        # Mousesssssssa
        surf = pygame.image.load(r"images\general\cursor.png").convert()
        cursor = pygame.cursors.Cursor((3, 3), surf)
        pygame.mouse.set_cursor(cursor)
        # General game stuff
        self.settings = json.load(open(r"scripts\settings.json"))
        self.background = pygame.image.load(r"images\general\background.png").convert()
        self.blackout = pygame.image.load(r'images/general/blackout.png').convert()
        self.blackout.set_alpha(255)
        self.clock = pygame.time.Clock()
        self.FPS = self.settings["FPS"]
        player_bindings = self.settings['key_bindings']
        self.bindings = [keys[player_bindings[0]],
                         keys[player_bindings[1]],
                         keys[player_bindings[2]],
                         keys[player_bindings[3]]]
        # Delta time
        self.dt = 0
        self.last_time = 0
        # Player
        self.player = Player(self.display, self.FPS)
        # The zombies ahhhhhhhhhhhhhh
        self.wave = 0
        self.zombies = []
        self.dead_zombies = []
        self.spawn_time_list = [9, 7, 15, 13, 9, 7, 3, 5, 7, 2, 3, 1, 2, 1]
        self.zombie_count = 0
        self.next_count = 1
        self.spawn_counter = time.time() + self.spawn_time_list[0]
        self.wave_counts = 0
        # HUD
        self.gun_hud = HUD(self.display, r'guns/', 'gun1',(self.display.get_rect().centerx, 20))
        self.hp_hud = HUD(self.display, r'health/', 'health4', (260, 20))
        # Medkit
        self.medkit_timer = time.time()
        self.medkit_time = random.randint(15, 23)
        self.medkit = None
        self.display_medkit = False
        self.medkit_particles = False
        self.m_particles = []
        # Score
        self.start_time = time.time()
        self.score = time.time() - self.start_time
        self.score_text = Text('images/general/black_font.png', (255, 255, 255))  # obj better
        # Number
        self.number = 14

    def _blackout(self, alpha):
        self.blackout.set_alpha(alpha)

    def _spawn_zombie(self, speed=1.25):
        self.zombies.append(Zombie(self.display, self.FPS, (
        0 if random.randint(0, 1) else self.display.get_width(), random.randint(16, self.display.get_height() - 16)),
                                   self.player.rect, self.player.mask, self.player.pos, speed))
        self.zombie_count += 1
        self.wave_counts += 1

    def _spawn_zombies(self):
        # So this is what makes it hard
        # 15 minutes
        if self.wave == 0:
            if len(self.spawn_time_list) != 0:
                if self.spawn_counter - time.time() <= 0:
                    self.next_count += 1
                    self.spawn_counter = time.time() + self.spawn_time_list[0]
                    del self.spawn_time_list[0]
                    self._spawn_zombie()
                if self.zombie_count == self.next_count and self.spawn_counter - time.time():
                    del self.spawn_time_list[0]
                    self.next_count += 1
                    self.spawn_counter = time.time() + self.spawn_time_list[0]
                    self._spawn_zombie()
            else:
                self.wave_counts = 0
                self.wave = 1
        if self.wave == 1:
            if self.wave_counts != 300:
                if random.randint(1, 25) == 12:
                    self._spawn_zombie(1.5)
            elif self.wave_counts == 300:  # yeah i'm aware
                self.wave_counts = 0
                self.wave = 2  # deal wit it
        if self.wave == 2:
            if self.wave_counts <= 600:
                if random.randint(1, 100) in [1, 15, 35, 55, 75, 100]:
                    self._spawn_zombie(1.75)
            else:
                self.wave_counts = 0
                self.wave += 1
        if self.wave == 3:
            if random.randint(1, 100) in [1, 15, 25, 35, 45, 55, 65, 75, 85, 100]:
                self._spawn_zombie(2.1)

    def _render_all(self):
        """Renders everything."""
        # Background
        self.display.blit(self.background, (0, 0))
        # Dead zombies so sad :(
        self.zombies.sort(key=lambda z: z.rect.centery)  # Love this trick
        for dead_zombie in self.dead_zombies:
            dead_zombie.render()
        # Medkit
        if self.medkit:
            self.medkit.render()
        # Player
        self.player.render()
        # Bullets
        for guns in self.player.guns.items():
            for bullet in guns[1].bullets:
                bullet.render()
        # Zombie
        for zombie in self.zombies:
            zombie.render()
        # Gun
        self.player.gun.render()
        # Particles
        for particle in self.m_particles:
            particle.render()
        # HUDs
        self.gun_hud.render()
        self.hp_hud.render()
        # Score
        self.score_text.render(self.display, str(round(self.score, 1)), (958, 690))
        # Blackout
        self.display.blit(self.blackout, (0, 0))

    def _update_all(self):
        """Updates everything."""
        # Delta time
        self.player.dt = self.dt
        self.player.gun.dt = self.dt
        for zombie in self.zombies:
            zombie.player_mask = self.player.mask
            zombie.dt = self.dt

        if self.blackout.get_alpha() != 0:
            self._blackout(self.blackout.get_alpha()-1)
        self.score = time.time() - self.start_time
        for dead_zombie in self.dead_zombies:
            dead_zombie.update()
        for zombie in self.zombies:
            if zombie.dead:
                self.dead_zombies.append(self.zombies.pop(self.zombies.index(zombie)))
            self.player.health += zombie.player_health
            zombie.player_health = 0
            zombie.player_pos = pygame.math.Vector2(self.player.rect.center)
            zombie.player_rect = self.player.rect
            for gun in self.player.guns.values():
                zombie.bullets += gun.bullets
            if zombie.kill == True:
                self.zombies.remove(zombie)
        # Player
        self.player.update()
        # Gun
        self.player.gun.update(pygame.math.Vector2(self.player.rect.center))
        # Bullets
        for gun in self.player.guns.items():
            gun[1].update_bullets()
        # Zombie
        for zombie in self.zombies:
            zombie.update()
        # Hud
        self.gun_hud.update(f'gun{self.player.gun_num}')
        self.hp_hud.update(f'health{self.player.health}')
        # Particles
        for particle in self.m_particles:
            particle.update()
            if particle.kill == True:
                del self.m_particles[self.m_particles.index(particle)] # FIX ME
        # DELETE ME
        self.player.health = 5

    def _game_over(self):
        game_over_screen = pygame.image.load('images\general\game_over.png')
        text = Text('images/general/white_font.png', (0, 0, 0))
        text2 = Text('images/general/white_font.png', (0, 0, 0))
        game_over_screen.set_alpha(0)
        gscreen = True
        while gscreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gscreen = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gscreen = False
                        break
            game_over_screen.set_alpha(game_over_screen.get_alpha()+1)
            self.display.blit(game_over_screen, (0, 0))
            text2.render(self.display,"Hah nerd you died loser imagine what was it too hard cry about it ",
                        (850, 100))
            text.render(self.display,
                        "yourmom doesn't want you and you have horrible sarcasm detection. ulrizbozo",
                        (780, 600))
            pygame.display.update()
            self.clock.tick(self.FPS)

    def run(self):
        """Handles the game loop."""
        running = True
        while running:
            # delta time/framerate independence
            self.dt = (time.time() - self.last_time) * self.TARGET_FPS
            self.last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse.get_pressed()[0] == 1:
                        self.player.gun.mouse_down = True
                    else:
                        self.player.gun.mouse_down = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.player.gun.mouse_down = False
                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        self.player.gun_num += -1 if self.player.gun_num - 1 > 0 else 3
                    else:
                        self.player.gun_num += 1 if self.player.gun_num + 1 < 5 else -3
            # Player movement y
            pressed_keys = pygame.key.get_pressed()
            if (pressed_keys[self.bindings[0]] and pressed_keys[self.bindings[1]]) or not (pressed_keys[self.bindings[0]] or pressed_keys[self.bindings[1]]):
                self.player.movement_y = 0
                self.player.gun.movement_y = 0
            elif pressed_keys[self.bindings[0]]:
                self.player.movement_y = -1
                self.player.gun.movement_y = -1
            elif pressed_keys[self.bindings[1]]:
                self.player.movement_y = 1
                self.player.gun.movement_y = 1
            # Player movement x
            if (pressed_keys[self.bindings[2]] and pressed_keys[self.bindings[3]]) or not (pressed_keys[self.bindings[2]] or pressed_keys[self.bindings[3]]):
                self.player.movement_x = 0
                self.player.gun.movement_x = 0
            elif pressed_keys[self.bindings[2]]:
                self.player.movement_x = -1
                self.player.gun.movement_x = -1
            elif pressed_keys[self.bindings[3]]:
                self.player.movement_x = 1
                self.player.gun.movement_x = 1
            # Gun
            if pressed_keys[pygame.K_1]:
                self.player.gun_num = 1
            if pressed_keys[pygame.K_2]:
                self.player.gun_num = 2
            if pressed_keys[pygame.K_3]:
                self.player.gun_num = 3
            if pressed_keys[pygame.K_4]:
                self.player.gun_num = 4
            # if pressed_keys[pygame.K_5]:
            #     self.player.gun_num = 5
            # if pressed_keys[pygame.K_6]:
            #     self.player.gun_num = 6

            for gun in self.player.guns.items():
                if gun[1] != self.player.gun:
                    gun[1].mouse_down = False

            # Medkit
            if not self.display_medkit and int(time.time() - self.medkit_timer) >= self.medkit_time:
                size = self.display.get_rect().size
                pos = (size[0] * random.uniform(0.15, 0.85), size[1] * random.uniform(0.15, 0.85))
                self.medkit = MedKit(self.display, pos)
                self.display_medkit = True
            if self.display_medkit and self.medkit.rect.colliderect(self.player.rect) and self.player.health != 5:
                if self.player.health == 4:
                    self.player.health += 1
                else:
                    self.player.health += 2
                self.medkit_particles = True
                self.m_particles = [
                    Particle(self.display, r'hud\health\health_particle.png', (self.medkit.rect.center[0] + random.randint(-12, 0), self.medkit.rect.center[1] + random.randint(-12, 12)), random.uniform(2.1, 2.6), math.radians(90), 0.37, size=True),
                    Particle(self.display, r'hud\health\health_particle.png', (self.medkit.rect.center[0] + random.randint(-3, 3), self.medkit.rect.center[1] + random.randint(-12, 12)), random.uniform(2.1, 2.6) + 0.2, math.radians(90), 0.35, size=True),
                    Particle(self.display, r'hud\health\health_particle.png', (self.medkit.rect.center[0] + random.randint(9, 12), self.medkit.rect.center[1] + random.randint(-12, 12)), random.uniform(2.1, 2.6), math.radians(90), 0.34, size=True)
                ]
                self.display_medkit = False
                self.medkit = None
                self.medkit_timer = time.time()
                self.medkit_time = random.randint(10, 20)

            self._update_all()
            self._spawn_zombies()
            self._render_all()
            self.clock.tick(self.FPS)
            pygame.display.update()
            if self.player.health <= 0:
                # Game over screen
                running = False
        if self.player.health <= 0:
            self._game_over()

        print("-48 Hours")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    zg = ZombieGame()
    zg.run()
