import pygame
from class_board import Board
from Load_image import load_image
from sprite_end import End
from sprite_truba import Truba
from sprite_nachlo import Nachalo
import sys


def zapolnenie(truba, nachalo, end, clock, sc, board):
    res = board.proverka()
    fon = load_image('фон_с_кнопками.png')
    sc.blit(fon, (0, 0))
    if res:
        for i in range(8):
            board.render(sc)
            nachalo.update()
            end.draw(sc)
            nachalo.draw(sc)
            truba.draw(sc)

            pygame.display.flip()
            clock.tick(8)
        for cord in res:
            if cord == res[-1]:
                fon = load_image('1_5.png')
                sc.blit(fon, (0, 0))
                pygame.display.flip()
                q = 0
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            if 0 <= event.pos[0] <= 638 and 609 <= event.pos[1] <= 609 + \
                                    110 and q == 0:
                                truba.update(faza_null=True)
                                fon = load_image('фон_с_кнопками.png')
                                sc.blit(fon, (0, 0))
                                board.render(sc)
                                truba.draw(sc)
                                nachalo.draw(sc)
                                end.draw(sc)
                                pygame.display.flip()
                                q += 1
                            if event.type == pygame.MOUSEBUTTONUP:
                                if q == 1:
                                    q += 1
                                elif q == 2:
                                    return True

            for i in range(9):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                truba.update(cord)
                truba.draw(sc)
                pygame.display.flip()
                clock.tick(30)


def level1(sc):
    fon = load_image('1_1.png')
    sc.blit(fon, (0, 0))
    pygame.display.flip()
    running = True
    board = Board(20, 14, [7, 3], [7, 0])
    board.set_view(0, 0, 32)
    q = 0
    truba = pygame.sprite.Group()
    end = pygame.sprite.Group()
    nachalo = pygame.sprite.Group()
    Nachalo(nachalo, 7)
    End(end, 4, 8)
    cord_button = [[831, 418, 113, 32], [640, 321, 640, 93]]
    sp_sprite = []
    shag = 1
    status = False
    sp_cord_level = [(1, 7), (2, 7)]
    sp = [(1, 7), (2, 7)]
    clock = pygame.time.Clock()

    while running:
        sc.fill((54, 54, 54))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and status is False:
                if cord_button[0][0] <= event.pos[0] <= cord_button[0][0] + cord_button[0][-2] and \
                        cord_button[0][1] <= event.pos[1] <= cord_button[0][1] + cord_button[0][-1]:
                    status = True
                    object = Truba(truba)
                    if shag == 1:
                        fon = load_image('1_2.png')
                        shag += 1
                elif cord_button[1][0] <= event.pos[0] <= cord_button[1][0] + cord_button[1][-2] and \
                        cord_button[1][1] <= event.pos[1] <= cord_button[1][1] + cord_button[1][-1] and shag == 5:
                    shag += 1
                    if zapolnenie(truba, nachalo, end, clock, sc, board):
                        return True


            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and status:
                if board.get_cell(event.pos):
                    pos = board.get_cell(event.pos)
                    if pos in sp_cord_level:
                        sp_cord_level.remove(pos)
                        status = False
                        object.stop(pos[0], pos[1])
                        board.take_a_position([pos[0], pos[1], object.get_position()])
                        if shag == 2:
                            fon = load_image('1_3.png')
                            shag += 1
                        elif shag == 3:
                            shag += 1
                        if shag == 4:
                            fon = load_image('1_4.png')
                            shag += 1
            if event.type == pygame.MOUSEMOTION and status:
                if board.get_cell(event.pos):
                    pos = board.get_cell(event.pos)
                    object.move(pos)

        board.render(sc)
        truba.draw(sc)
        nachalo.draw(sc)
        end.draw(sc)
        sc.blit(fon, (0, 0))
        pygame.display.flip()
