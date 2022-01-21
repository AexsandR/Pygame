import pygame
from Load_image import load_image


class Ventilator(pygame.sprite.Sprite):
    def __init__(self, sprite, pos_in_mas=False):
        super().__init__(sprite)
        self.image = load_image('вентилятор 0.png')
        self.rect = self.image.get_rect()
        self.angle = -90
        self.sprite = sprite
        self.rect.x = 0
        self.rect.y = 0
        self.position = ['-', '|']
        self.position_in_masiv = 0
        self.status_move = True
        self.cur_frame = 0
        self.frame = []
        self.x = None
        self.y = None
        self.stutus_naprovlenie = False
        if pos_in_mas:
            for i in range(len(self.position)):
                if pos_in_mas == self.position[i]:
                    self.position_in_masiv = i
                    break

    def cut_sheet(self, angle):
        for i in range(3):
            self.image = load_image(f'вентилятор {i}.png')
            self.rect = self.image.get_rect()
            self.image = pygame.transform.rotate(self.image, angle)
            self.frame.append(self.image)

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

    def stop(self, x, y):
        print(self.position[self.position_in_masiv])
        self.status_move = False
        self.x = x
        print(x)
        self.y = y
        if self.position[self.position_in_masiv] == '|':
            self.image = load_image('вентилятор 0.png')
            self.image = pygame.transform.rotate(self.image, -90)
            self.cut_sheet(-90)
            self.image = self.frame[self.cur_frame]
            self.rect.x = x * 32
            self.rect.y = y * 32
            print(self.rect.x)
        else:
            self.image = load_image('вентилятор 0.png')
            self.cut_sheet(0)
            self.image = self.frame[self.cur_frame]
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

        if clear:
            self.kill()
        elif spisok[0] == self.x and self.y == spisok[1]:
            if dell:
                self.kill()
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
