import pygame
from class_board import Board
from Load_image import load_image
from sprite_end import End
from sprite_truba import Truba
from sprite_nachlo import Nachalo



def level3(sc):
    fon = load_image('3_1.png')
    sc.blit(fon, (0, 0))
    pygame.display.flip()
    board = Board(20, 14, [8, 0], [6, 0])
    board.set_view(0, 0, 32)
    nachalo = pygame.sprite.Group()
    Nachalo(nachalo, 7)
    end = pygame.sprite.Group()
    End(end, 5, 8)
    truba = pygame.sprite.Group()
    shag = 1
    while True:
        sc.fill((54, 54, 54))
        board.render(sc)
        sc.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and shag == 1:
                if board.get_cell(event.pos):
                    pos = board.get_cell(event.pos)
                    if pos == (1, 7):
                        shag += 1
                        fon = load_image('3_2.png')
                        sc.blit(fon, (0, 0))
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and shag == 2:
                if board.get_cell(event.pos):
                    pos = board.get_cell(event.pos)
                    if pos == (3, 7):
                        object = Truba(truba)
                        object.move((1, 7))
                        object.stop(1,7)
                        object = Truba(truba)
                        object.move((2, 7))
                        object = Truba(truba)
                        object.move((3, 7))
                        shag += 1
                        fon = load_image('3_3.png')
                        sc.blit(fon, (0, 0))
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and shag == 3:
                shag += 1
                fon = load_image('3_4.png')
                sc.blit(fon, (0, 0))
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and shag == 4:
                if 960 <= event.pos[0] <= 960 +319 and 161 <= event.pos[1] <= 161 +159:
                    shag += 1
                    [641, 1, 318, 159]
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and shag == 5:
                pos = board.get_cell(event.pos)
                print(pos)
                if pos == (1, 7):
                    truba.update(pos, dell=True)
                    fon = load_image('3_5.png')
                    sc.blit(fon, (0, 0))
                    shag += 1
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and shag == 6:
                if 641 <= event.pos[0] <= 641 + 318 and 1 <= event.pos[1] <= 1 + 159:
                    object = Truba(truba)
                    object.move((1, 7))
                    shag +=1
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and shag == 7:
                return  True

        nachalo.draw(sc)
        end.draw(sc)
        truba.draw(sc)
        pygame.display.flip()

