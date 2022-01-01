import pygame
from Load_image import load_image


class End(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(type)
        self.image = load_image('конец.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect.x = (x - 1) * 32
        self.rect.y = (y - 1) * 32
