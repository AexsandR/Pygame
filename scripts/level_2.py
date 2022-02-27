import pygame
from class_board import Board
from Load_image import load_image
from sprite_end import End
from sprite_truba import Truba
from sprite_nachlo import Nachalo
from sprite_angle import Angle



def level2(sc):
    fon = load_image('2_1.png')
    sc.blit(fon, (0, 0))
    pygame.display.flip()
    board = Board(20, 14, [8, 0], [6, 0])
    board.set_view(0, 0, 32)
    q = 0
    end = pygame.sprite.Group()
    nachalo = pygame.sprite.Group()
    Nachalo(nachalo, 6)
    End(end, 1, 9)
    truba = pygame.sprite.Group()
    angle = pygame.sprite.Group()
    running = True
    status = False
    cord_button = [[1121, 418, 159, 40], [831, 418, 113, 32], [320, 448, 319, 112], [1, 448, 319, 112]]
    sp_cord_level = [(1, 6), (1, 7), (1, 8)]
    shag = 1
    q = 0
    while running:
        sc.fill((54, 54, 54))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and status and shag == 5:
                if cord_button[2][0] <= event.pos[0] <= cord_button[2][0] + cord_button[2][-2] and \
                        cord_button[2][1] <= event.pos[1] <= cord_button[2][1] + cord_button[2][
                    -1]:
                    object.rotate(-1)
                    shag += 1
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and status and 11 > shag >= 8:
                if cord_button[3][0] <= event.pos[0] <= cord_button[3][0] + cord_button[3][-2] and \
                        cord_button[3][1] <= event.pos[1] <= cord_button[3][1] + cord_button[2][
                    -1]:
                    object.rotate(1)
                    shag += 1
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and status is False:
                if cord_button[0][0] <= event.pos[0] <= cord_button[0][0] + cord_button[0][-2] and \
                        cord_button[0][1] <= event.pos[1] <= cord_button[0][1] + cord_button[0][-1] and (
                        shag == 1 or shag == 7):
                    status = True
                    object = Angle(angle)
                    shag += 1
                elif cord_button[1][0] <= event.pos[0] <= cord_button[1][0] + cord_button[1][-2] and \
                        cord_button[1][1] <= event.pos[1] <= cord_button[1][1] + cord_button[1][-1] and shag == 3:
                    status = True
                    object = Truba(truba)
                    shag += 1

            if event.type == pygame.MOUSEMOTION and status:
                if board.get_cell(event.pos):
                    pos = board.get_cell(event.pos)
                    object.move(pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and status and shag != 5:
                if board.get_cell(event.pos):
                    pos = board.get_cell(event.pos)
                    if pos in sp_cord_level and pos == sp_cord_level[0]:
                        if shag == 4:
                            shag += 1
                            fon = load_image('2_3.png')
                            sc.blit(fon, (0, 0))
                        else:
                            sp_cord_level.remove(pos)
                            status = False
                            object.stop(pos[0], pos[1])
                            board.take_a_position([pos[0], pos[1], object.get_position()])
                            if shag == 2:
                                fon = load_image('2_2.png')
                                sc.blit(fon, (0, 0))
                                shag += 1
                            if shag == 6:
                                fon = load_image('2_4.png')
                                sc.blit(fon, (0, 0))
                                shag += 1
                            if shag == 11:
                                shag += 1
                            if shag == 12:
                                return True

        board.render(sc)
        end.draw(sc)
        nachalo.draw(sc)
        angle.draw(sc)
        truba.draw(sc)
        sc.blit(fon, (0, 0))
        pygame.display.flip()
