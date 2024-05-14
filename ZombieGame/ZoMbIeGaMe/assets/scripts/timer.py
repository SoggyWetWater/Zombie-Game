import time

import pygame

class Timer:
    def __init__(self, display):
        self.display = display
        self.surf = pygame.Surface((8, 8))
        self.image = 0# haha ima wrroi about this later
        #self.rect = self.image.get_frect()
        self.start_time = time.time()
        self.current_time = time.time()

  #  for digit in str(self.timer):
       #     self.

    def update(self):
        pass

  #     self.display.blit(self.image, self.rect)