import pygame

from Start_window import start_screen
from Load_image import load_image


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
                        import vodoprovod
                        running = False
                    else:
                       import level_1


if __name__ != '__main__':
    menu()
