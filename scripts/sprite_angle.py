import pygame
from Load_image import load_image


class Angle(pygame.sprite.Sprite):
    def __init__(self, sprite, pos_in_mas=False):
        super().__init__(sprite)
        self.image = load_image('угол 0.png')
        self.rect = self.image.get_rect()
        self.rect.x = -200
        self.rect.y = -100
        self.status_move = True
        self.position = ['>|', '-|', '|-', '|>']
        self.position_in_masiv = 0
        self.cur_frame = 0
        self.frame = []
        self.cut_sheet()
        self.image = self.frame[self.cur_frame]

        if pos_in_mas:
            for i in range(len(self.position)):
                if pos_in_mas == self.position[i]:
                    self.position_in_masiv = i
                    self.image = pygame.transform.rotate(self.image, 90 * i)
                    print(12312354675467)
                    print(i)
                    break

    def cut_sheet(self):
        for i in range(10):
            self.image = load_image(f'угол {i}.png')
            self.rect = self.image.get_rect()
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
        self.status_move = False
        self.x = x
        self.y = y

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

    def update(self, spisok=[-1, -1], dell=False, clear=False):
        if clear:
            self.kill()
        if self.x == spisok[0] and self.y == spisok[1]:
            if dell:
                self.kill()
            elif spisok[2] == 'right' and spisok[3] == 'down':
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
                self.image = pygame.transform.rotate(self.image, 90)
                self.image = pygame.transform.flip(self.image, True, False)

            elif spisok[2] == 'right' and spisok[3] == 'up':
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
                self.image = pygame.transform.rotate(self.image, -90)
            elif spisok[2] == 'down' and spisok[3] == 'left':
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
                self.image = pygame.transform.flip(self.image, False, True)

            elif spisok[2] == 'down' and spisok[3] == 'right':
                print(2342)
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
                self.image = pygame.transform.flip(self.image, True, True)
            elif spisok[2] == 'left' and spisok[3] == 'up':
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
                self.image = pygame.transform.flip(self.image, False, True)
                self.image = pygame.transform.rotate(self.image, -90)

            elif spisok[2] == 'left' and spisok[3] == 'down':
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
                self.image = pygame.transform.flip(self.image, False, False)
                self.image = pygame.transform.rotate(self.image, 90)
            elif spisok[2] == 'up' and spisok[3] == 'right':
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                print(000)
                print(spisok)
                self.cur_frame = (self.cur_frame + 1) % len(self.frame)
                self.image = self.frame[self.cur_frame]
