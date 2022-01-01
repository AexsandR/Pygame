import pygame
from Load_image import load_image
class Truba(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__(type)
        self.image = load_image('заполнение 0.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect.x = -100
        self.rect.y = -100
    def update(self, sp):
        action = sp[0]
        if action == 'перемещение':
            self.rect.x = sp[1] * 32
            self.rect.y = sp[2] * 32
            print(self.rect.x)
        elif action == 'поворт':
            self.image = pygame.transform.rotate(self.image, -90)



