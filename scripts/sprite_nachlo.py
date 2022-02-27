import pygame
from Load_image import load_image


class Nachalo(pygame.sprite.Sprite):
    def __init__(self, type, y):
        super().__init__(type)
        self.image = load_image('начало 0.png')
        self.image = pygame.transform.rotate(self.image, 90)
        self.frame = []
        self.cut_sheet()
        self.cur_frame = 0
        self.image = self.frame[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y * 32

    def rotate(self, q):
        if q == 1:
            self.image = pygame.transform.rotate(self.image, 90)
            self.position_in_masiv = (1 + self.position_in_masiv) % len(self.position)
        else:
            self.image = pygame.transform.rotate(self.image, -90)
            self.position_in_masiv = (-1 + self.position_in_masiv) % len(self.position)

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
