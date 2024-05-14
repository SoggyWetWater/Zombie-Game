"""Frick billy"""

import pygame


class HUD:
    """So that's probably not how you do it"""
    def __init__(self, display, file_path, img, pos):
        """Cool"""
        self.display = display
        self.img = img
        self.file_path = file_path
        self.image = pygame.image.load(r'images/hud/' + file_path + img + r'.png')
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_frect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_alpha(191)
        self.pos = pos

    def update(self, img):
        """Get updated"""
        self.image = pygame.image.load(r'images/hud/' + self.file_path + img + r'.png')
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.image.set_alpha(191)

    def render(self):
        """Get rendered"""
        self.display.blit(self.image, self.rect)
