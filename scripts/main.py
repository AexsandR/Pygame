import pygame
from Start_window import start_screen
from class_board import Board
from sprite_nachlo import Nachalo
from sprite_end import End
from sprite_truba import Truba
import sys


def zapolnenie():
    for i in range(9):
        board.render(screen)
        nachalo.update()
        end.draw(screen)
        nachalo.draw(screen)
        pygame.display.flip()
        clock.tick(2)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    nachalo = pygame.sprite.Group()
    truba = pygame.sprite.Group()
    end = pygame.sprite.Group()
    smesitel = pygame.sprite.Group()
    Nachalo(nachalo)
    End(end, 20, 14)
    x = 0
    y = 0
    if start_screen(screen):
        board = Board(20, 14)
        board.set_view(0, 0, 32)
        running = True
        while running:
            screen.fill((54, 54, 54))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if 0 <= event.pos[0] <= 32 and 0 <= event.pos[1] <= 32:
                        zapolnenie()
                if event.type == pygame.MOUSEMOTION:
                    if board.get_cell(event.pos):
                        pos = board.get_cell(event.pos)
                        truba.update(['перемещение', pos[0], pos[1]])
                if event.type == pygame.KEYUP and event.key == pygame.K_1:
                    Truba(truba)
                    print(1)
            board.render(screen)
            nachalo.draw(screen)
            end.draw(screen)
            truba.draw(screen)
            pygame.display.flip()
