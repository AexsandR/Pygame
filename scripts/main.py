from Start_window import start_screen
from class_board import Board
from sprite_nachlo import Nachalo
from sprite_end import End
from sprite_truba import *
from sprite_angle import Angle
import sys


def zapolnenie():
    for i in range(8):
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


def proverka_sp(pos, type_sprite):
    global status
    if object.proverka([truba, nachalo, end, smesitel, angle]):
        status = False
        try:
            board.take_a_position([pos[0], pos[1], object.get_position()])
        except Exception as er:
            print(er)
            board.take_a_position([pos[0], pos[1], object.get_position()])
            object.stop(pos[0], pos[1])
            list_action.append([pos[0], pos[1]])
            all_sprites.remove(object)
        else:
            object.stop(pos[0], pos[1])
            list_action.append([pos[0], pos[1]])
            all_sprites.remove(object)
            truba.add(object)
            print(all_sprites)
            print(truba)


def proverka_combo(x, y):
    if object.proverka([truba, nachalo, end, smesitel, angle]):
        try:
            board.take_a_position([x, y, object.get_position()])
        except Exception as er:
            print(er)
            board.take_a_position([x, y, object.get_position()])
            object.stop(x, y)
            all_sprites.remove(object)
            truba.add(object)
        else:
            object.stop(x, y)
            all_sprites.remove(object)
            truba.add(object)
            return True
    else:
        object.kill()


if __name__ == '__main__':
    board = Board(20, 14)
    board.set_view(0, 0, 32)
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    fon = pygame.transform.scale(load_image('фон_с_кнопками.png'), (1280, 720))
    clock = pygame.time.Clock()
    nachalo = pygame.sprite.Group()
    truba = pygame.sprite.Group()
    end = pygame.sprite.Group()
    smesitel = pygame.sprite.Group()
    angle = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    status_combo = False
    SPISOK_BUTTON = [[[641, 1, 318, 159], 'Действие назад', None], [[960, 1, 319, 159], 'Сохранить'],
                     [[641, 161, 319, 159], 'Очистить поле',None], [[960, 161, 319, 159], 'Удалить обьект', None],
                     [[640, 321, 640, 93], 'Заполнение', zapolnenie], [[640, 411, 190, 36], 'Вентилятор'],
                     [[831, 411, 113, 36], Truba, truba, None],
                     [[944, 411, 176, 36], 'смеситель'], [[1121, 411, 159, 36], Angle, angle, None]]

    Nachalo(nachalo)
    End(end, 20, 1)
    fps_volt = 60
    fps_amper = fps_volt
    x_combo = None
    y_combo = None
    status_dell = False
    x = 0
    y = 0
    all_sprites = pygame.sprite.Group()
    spisok_number_combo_in_list_action = []
    list_action = []
    if start_screen(screen):
        running = True
        status = False
        while running:
            screen.fill((54, 54, 54))
            screen.blit(fon, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if status:
                        pos = board.get_cell(event.pos)
                        if pos:
                            proverka_sp(pos, type_sprite)
                    if status_dell and status_combo is False:
                        pos = board.get_cell(event.pos)
                        if pos:
                            pos = list(pos)
                            if pos in list_action:
                                angle.update(pos,dell=True)
                                truba.update(pos, dell=True)
                                list_action.remove(pos)
                                board.take_a_position([pos[0], pos[1], 0])
                            else:
                                for i in spisok_number_combo_in_list_action:
                                    if pos in list_action[i]:
                                        angle.update(pos, dell=True)
                                        truba.update(pos, dell=True)
                                        list_action[i].remove(pos)
                                        board.take_a_position([pos[0], pos[1], 0])
                                        break

                    if status_combo:
                        status_dell = False
                        pos = board.get_cell(event.pos)
                        if pos:
                            if pos[0] == x_combo and pos[1] != y_combo:
                                razniza = max([y_combo, pos[1]]) - min([y_combo, pos[1]])
                                status_combo = False
                                for i in range(razniza + 1):
                                    object = Truba(all_sprites)
                                    object.move([x_combo, min([y_combo, pos[1]]) + i])
                                    object.rotate(-1)
                                    res = proverka_combo(x_combo, min([y_combo, pos[1]]) + i)
                                    if res:
                                        sp.append([x_combo, min([y_combo, pos[1]]) + i])
                                spisok_number_combo_in_list_action.append(len(list_action))
                                list_action.append(sp)
                            elif pos[0] != x_combo and pos[1] == y_combo:
                                razniza = max([x_combo, pos[0]]) - min([x_combo, pos[0]])
                                status_combo = False
                                sp = []
                                for i in range(razniza + 1):
                                    object = Truba(all_sprites)
                                    object.move([max([x_combo, pos[0]]) - i, y_combo])
                                    res = proverka_combo(max([x_combo, pos[0]]) - i, y_combo)
                                    if res:
                                        sp.append([max([x_combo, pos[0]]) - i, y_combo])
                                spisok_number_combo_in_list_action.append(len(list_action))
                                list_action.append(sp)
                            else:
                                status_combo = False
                        else:
                            status_combo = False
                    else:
                        status_combo = False
                        print(status)
                        for i in SPISOK_BUTTON:
                            if i[0][0] <= event.pos[0] <= i[0][0] + i[0][2] and i[0][1] <= event.pos[1] <= i[0][1] + \
                                    i[0][3]:
                                if len(i) == 3:
                                    if i[1] == 'Заполнение':
                                        i[2]()
                                    elif i[1] == 'Действие назад':
                                        if len(list_action) != 0:
                                            elem = list_action.pop()
                                            if type(elem) == list:
                                                for i in elem:
                                                    truba.update(i, dell=True)
                                                    board.take_a_position([i[0], i[1], 0])
                                            else:
                                                truba.update(elem, dell=True)
                                                board.take_a_position([elem[0], elem[1], 0])
                                    elif i[1] == 'Удалить обьект':
                                        status_dell = True
                                    elif i[1] == 'Очистить поле':
                                        truba.update(clear=True)
                                        angle.update(clear=True)
                                        board.new_pole()
                                        list_action = []
                                        spisok_number_combo_in_list_action = []


                                else:
                                    if status is False:
                                        object = i[1](all_sprites)
                                        type_sprite = i[-1]
                                        status_combo = False
                                        status = True
                                        status_dell = False

                if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and status_combo is False and status is False:
                    pos = board.get_cell(event.pos)
                    x_combo = pos[0]
                    y_combo = pos[1]
                    status_combo = True
                if event.type == pygame.KEYUP and event.key == pygame.K_o and status and status_combo is False:
                    object.rotate(1)
                elif event.type == pygame.KEYUP and event.key == pygame.K_p and status and status_combo is False:
                    object.rotate(-1)

                if event.type == pygame.MOUSEMOTION and status:
                    if board.get_cell(event.pos):
                        pos = board.get_cell(event.pos)
                        object.move(pos)

            board.render(screen)
            nachalo.draw(screen)
            end.draw(screen)
            all_sprites.draw(screen)
            truba.draw(screen)
            pygame.display.flip()
