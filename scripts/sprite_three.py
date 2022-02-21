import pygame
from Load_image import load_image


class Three(pygame.sprite.Sprite):
    def __init__(self, sprite, pos_in_mas=0):
        super().__init__(sprite)
        self.image = load_image('тройник.png')
        self.rect = self.image.get_rect()
        self.angle = -90
        self.sprite = sprite
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect.x = 0
        self.rect.y = 0
        self.position = ["-^-", "|>|", "-v-", "|<|"]
        self.position_in_masiv = pos_in_mas

    def move(self, sp):
        self.rect.x = sp[0] * 32
        self.rect.y = sp[1] * 32

    def rotate(self, q):
        if q == 1:
            self.image = pygame.transform.rotate(self.image, 90)
            self.position_in_masiv = (-1 + self.position_in_masiv) % len(self.position)
        else:
            self.image = pygame.transform.rotate(self.image, -90)
            self.position_in_masiv = (1 + self.position_in_masiv) % len(self.position)

    def stop(self, x, y):
        self.status_move = False
        self.x = x
        self.y = y
        self.rect.x = x * 32
        self.rect.y = y * 32

    def proverka(self, sp):
        q = 0
        for i in sp:
            if pygame.sprite.spritecollideany(self, i):
                q += 1
                break
        if q == 0:
            return True
        else:
            return False

    def get_position(self):
        return self.position[self.position_in_masiv]

    def update(self, spisok=[-1, -1], dell=False, clear=False, faza_null=False):
        if faza_null:
            self.cur_frame = 0
            self.image = self.frame[self.cur_frame]
        elif clear:
            self.kill()
        elif spisok[0] == self.x and self.y == spisok[1]:
            if dell:
                self.kill()