"""U wanna get healed yay or nay cause im fine with nay"""
import pygame

class MedKit:
    """Honestly who cares at this point."""
    def __init__(self, display, pos):
        """Hahjhahah yeah, its this thing"""
        self.display = display
        self.image = pygame.image.load(r'images\general\medkit.png')
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.heal = False

    def render(self):
        """Oohh you know this one."""
        self.display.blit(self.image, self.pos)