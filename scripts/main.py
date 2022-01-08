from Start_window import start_screen
from class_board import Board
from sprite_nachlo import Nachalo
from sprite_end import End
from sprite_truba import *
from sprite_angle import Angle
import sys


def zapolnenie():
    for i in range(9):
        board.render(screen)
        nachalo.update()
        end.draw(screen)
        nachalo.draw(screen)
        truba.draw(screen)
        angle.draw(screen)
        pygame.display.flip()
        clock.tick(8)
    res = board.proverka()
    if res:
        for cord in res:
            for i in range(9):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                truba.update(cord)
                angle.update(cord)
                truba.draw(screen)
                angle.draw(screen)
                pygame.display.flip()
                clock.tick(60)


def proverka_sp(pos):
    global status
    if object.proverka([truba, nachalo, end, smesitel, angle]):
        status = False
        try:
            board.take_a_position([pos[0], pos[1], object.get_position()])
        except Exception as er:
            print(er)
            board.take_a_position([pos[0], pos[1], object.get_position()])
            object.stop(pos[0], pos[1])
        else:
            object.stop(pos[0], pos[1])

def proverka_combo(x,y):
    if object.proverka([truba, nachalo, end, smesitel, angle]):
        try:
            board.take_a_position([x, y, object.get_position()])
        except Exception as er:
            print(er)
            board.take_a_position([x, y, object.get_position()])
            object.stop(x, y)
        else:
            object.stop(x,y)
    else:
        object.move([-100,-100])
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    nachalo = pygame.sprite.Group()
    truba = pygame.sprite.Group()
    end = pygame.sprite.Group()
    smesitel = pygame.sprite.Group()
    angle = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    status_combo = False
    Nachalo(nachalo)
    End(end, 20, 1)
    x_combo = None
    y_combo = None
    x = 0
    y = 0
    if start_screen(screen):
        board = Board(20, 14)
        board.set_view(0, 0, 32)
        running = True
        status = False
        while running:
            screen.fill((54, 54, 54))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if 0 <= event.pos[0] <= 32 and 0 <= event.pos[1] <= 32 and status is False:
                        zapolnenie()
                    if status:
                        proverka_sp(pos=board.get_cell(event.pos))
                    if status_combo:
                        print(123)
                        pos = board.get_cell(event.pos)

                        if pos[0] == x_combo and pos[1] != y_combo:
                            razniza = max([y_combo, pos[1]]) - min([y_combo, pos[1]])
                            status_combo = False
                            for i in range(razniza + 1):
                                object = Truba(all_sprites, truba)
                                object.move([x_combo, min([y_combo, pos[1]]) + i])
                                object.rotate(-1)
                                proverka_combo(x_combo, min([y_combo, pos[1]]) + i)
                        elif pos[0] != x_combo and pos[1] == y_combo:
                            razniza = max([x_combo, pos[0]]) - min([x_combo, pos[0]])
                            status_combo = False
                            for i in range(razniza + 1):
                                object = Truba(all_sprites, truba)
                                object.move([max([x_combo, pos[0]]) - i, y_combo])
                                proverka_combo(max([x_combo, pos[0]]) - i, y_combo)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and status_combo is False and status is False:
                    print(1234)
                    pos = board.get_cell(event.pos)
                    x_combo = pos[0]
                    y_combo = pos[1]
                    status_combo = True
                if event.type == pygame.KEYUP and event.key == pygame.K_o and status and status_combo is False:
                    object.rotate(1)
                elif event.type == pygame.KEYUP and event.key == pygame.K_p and status and status_combo is False:
                    object.rotate(-1)

                if event.type == pygame.MOUSEMOTION and status and status_combo is False:
                    if board.get_cell(event.pos):
                        pos = board.get_cell(event.pos)
                        object.move(pos)
                if event.type == pygame.KEYUP and event.key == pygame.K_1 and status is False:
                    status = True
                    print(12)
                    object = Truba(all_sprites, truba)
                if event.type == pygame.KEYUP and event.key == pygame.K_2 and status is False:
                    status = True
                    print(12)
                    object = Angle(all_sprites, angle)
            board.render(screen)
            nachalo.draw(screen)
            end.draw(screen)
            all_sprites.draw(screen)
            truba.draw(screen)
            pygame.display.flip()
