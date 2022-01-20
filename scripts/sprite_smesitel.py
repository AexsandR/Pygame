import pygame
from Load_image import load_image


class Smesitel(pygame.sprite.Sprite):
    def __init__(self, sprite, pos_in_mas=False):
        super().__init__(sprite)
        self.image = load_image('смеситель 0.png')
        self.rect = self.image.get_rect()
        self.angle = -90
        self.sprite = sprite
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect.x = -100
        self.rect.y = -100
        self.position = ['-', '|']
        self.position_in_masiv = 0
        self.status_move = True
        self.cur_frame = 0
        self.frame = []
        self.x = None
        self.y = None
        self.stutus_naprovlenie = False
        self.cut_sheet()
        self.image = self.frame[self.cur_frame]
        if pos_in_mas:
            for i in range(len(self.position)):
                if pos_in_mas == self.position[i]:
                    self.position_in_masiv = i
                    self.image = pygame.transform.rotate(self.image, 90 * i)
                    break

    def rotate(self, q):
        if q == 1:
            self.image = pygame.transform.rotate(self.image, 90)
            self.position_in_masiv = (1 + self.position_in_masiv) % len(self.position)
        else:
            self.image = pygame.transform.rotate(self.image, -90)
            self.position_in_masiv = (-1 + self.position_in_masiv) % len(self.position)

    def cut_sheet(self):
        for i in range(5):
            self.image = load_image(f'смеситель {i}.png')
            self.rect = self.image.get_rect()
            self.image = pygame.transform.rotate(self.image, -90)
            self.frame.append(self.image)

    def stop(self, x, y):
        self.status_move = False
        self.x = x
        self.y = y

    def move(self, sp):
        self.rect.x = sp[0] * 32
        self.rect.y = sp[1] * 32

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

    def update(self, spisok=[-1, -1], dell=False, clear=False):
        print(spisok)
        if clear:
            self.kill()
        if spisok[0] == self.x and self.y == spisok[1]:
            if dell:
                self.kill()
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
