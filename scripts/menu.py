import pygame

from Start_window import start_screen
from Load_image import load_image
from level_1 import level1
from level_2 import level2
from level_3 import level3
from vodoprovod import start


def menu():
    pygame.init()
    sc = pygame.display.set_mode((1280, 720))
    if start_screen(sc):
        print('yes')
        fon = load_image('menu.png')
        sc.blit(fon, (0, 0))
        pygame.display.flip()
        running = True
        q = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP and q == 0:
                    q += 1
                elif event.type == pygame.MOUSEBUTTONUP and q != 0:
                    if 0 <= event.pos[1] < 301:
                        start(sc)
                        return None
                    else:
                        if level1(sc):
                            if level2(sc):
                                if level3(sc):
                                    if start(sc):
                                        return None
                        return None


if __name__ != '__main__':
    menu()
