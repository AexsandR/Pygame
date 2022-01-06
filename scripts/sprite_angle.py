import pygame
from Load_image import load_image


class Angle(pygame.sprite.Sprite):
    def __init__(self, sprite, type):
        super().__init__(sprite)
        self.image = load_image('угол.png')
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100
        self.type = type
        self.status_move = True
        self.position = ['>|', '-|', '|-', '|>']
        self.position_in_masiv = 0

    def move(self, sp):
        self.rect.x = sp[0] * 32
        self.rect.y = sp[1] * 32

    def rotate(self, q):
        if q == 1:
            self.image = pygame.transform.rotate(self.image, 90)
            self.position_in_masiv = (1 + self.position_in_masiv) % len(self.position)
        else:
            self.image = pygame.transform.rotate(self.image, -90)
            self.position_in_masiv = (-1 + self.position_in_masiv) % len(self.position)

    def stop(self):
        self.status_move = False
        self.add(self.type)

    def get_position(self):
        return self.position[self.position_in_masiv]

    def proverka(self, sp):
        q = 0
        for i in sp:
            if pygame.sprite.spritecollideany(self, i):
                q += 1
        if q == 0:
            return True
        else:
            return False

    def update(self, naprovlenie):
        ...
