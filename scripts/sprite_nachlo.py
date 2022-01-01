import pygame
from Load_image import load_image


class Nachalo(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__(type)
        self.image = load_image('начало 0.png')
        self.rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect.x = 0
        self.rect.y = 0
        self.frame = []
        self.cut_sheet()
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]

    def cut_sheet(self):
        for i in range(9):
            if i == 8:
                self.image = load_image(f'начало 0.png')
                self.image = pygame.transform.rotate(self.image, 90)
            else:
                self.image = load_image(f'начало {i}.png')
                self.rect = self.image.get_rect()
                self.image = pygame.transform.rotate(self.image, 90)
            self.frame.append(self.image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frame)
        self.image = self.frame[self.cur_frame]
