from Start_window import start_screen
from class_board import Board
from sprite_nachlo import Nachalo
from sprite_end import End
from sprite_truba import *
from sprite_angle import Angle
import sys
from Posledovatelnoe_connect import posledovatelnoe_connect_om
from sprite_smesitel import Smesitel


def zapolnenie(fps_volt):
    res = board.proverka()
    if res:
        for i in range(8):
            board.render(screen)
            nachalo.update()
            end.draw(screen)
            nachalo.draw(screen)
            truba.draw(screen)
            angle.draw(screen)
            smesitel.draw(screen)
            pygame.display.flip()
            clock.tick(8)
        fps_amper = posledovatelnoe_connect_om(res, slovar_smesitel, fps_volt)
        print(fps_amper)
        for cord in res:
            tmp = (cord[0], cord[1])
            if tmp in slovar_smesitel:
                fps_volt = fps_amper * slovar_smesitel[tmp]
            for i in range(9):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                truba.update(cord)
                angle.update(cord)
                truba.draw(screen)
                angle.draw(screen)
                smesitel.draw(screen)
                pygame.display.flip()
                clock.tick(fps_amper)


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
            type_sprite.add(object)
        else:
            object.stop(pos[0], pos[1])
            list_action.append([pos[0], pos[1]])
            all_sprites.remove(object)
            type_sprite.add(object)
            if type_sprite == smesitel:
                slovar_smesitel[(pos[0], pos[1])] = 0
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
                     [[641, 161, 319, 159], 'Очистить поле', None], [[960, 161, 319, 159], 'Удалить обьект', None],
                     [[640, 321, 640, 93], 'Заполнение', zapolnenie], [[640, 411, 190, 36], 'Вентилятор'],
                     [[831, 418, 113, 40], Truba, truba, None],
                     [[944, 418, 176, 40], Smesitel, smesitel, None], [[1121, 418, 159, 40], Angle, angle, None]]

    Nachalo(nachalo)
    End(end, 1, 8)
    fps_volt = 60
    fps_amper = fps_volt
    x_combo = None
    y_combo = None
    status_dell = False
    fps_volt = 60
    x = 0
    y = 0
    all_sprites = pygame.sprite.Group()
    spisok_number_combo_in_list_action = []
    list_action = []
    slovar_smesitel = {}
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
                    pos = board.get_cell(event.pos)
                    if pos:
                        print('ok')
                        print(slovar_smesitel)
                        if (pos[0], pos[1]) in slovar_smesitel:
                            slovar_smesitel[(pos[0], pos[1])] = (slovar_smesitel[(pos[0], pos[1])] + 1) % 5
                            smesitel.update(pos)
                    if status:
                        pos = board.get_cell(event.pos)
                        if pos:
                            proverka_sp(pos, type_sprite)
                    if status_dell and status_combo is False:
                        pos = board.get_cell(event.pos)
                        if pos:
                            pos = list(pos)
                            if pos in list_action:
                                len_truba = len(truba)
                                len_angle = len(angle)
                                truba.update(pos, dell=True)
                                angle.update(pos, dell=True)
                                res = list_action.index(pos)
                                print(res)
                                list_action[res] = None
                                if len_truba - 1 == len(truba):
                                    pos.append(Truba)
                                    pos.append(truba)
                                    pos.append(board.to_give_position([pos[0], pos[1]]))
                                elif len_angle - 1 == len(angle):
                                    pos.append(Angle)
                                    pos.append(angle)
                                    pos.append(board.to_give_position([pos[0], pos[1]]))
                                print()
                                print(pos)
                                pos.append(res)
                                list_action.append(pos)
                                print(list_action)
                                board.take_a_position([pos[0], pos[1], 0])
                            else:
                                for i in spisok_number_combo_in_list_action:
                                    if pos in list_action[i]:
                                        truba.update(pos, dell=True)
                                        res = list_action[i].index(pos)
                                        list_action[i][res] = None
                                        pos.append(Truba)
                                        pos.append(truba)
                                        pos.append(board.to_give_position([pos[0], pos[1]]))
                                        pos.append(i)
                                        pos.append(res)
                                        list_action.append(pos)
                                        board.take_a_position([pos[0], pos[1], 0])
                                        break

                    if status_combo:
                        status_dell = False
                        pos = board.get_cell(event.pos)
                        if pos:
                            if pos[0] == x_combo and pos[1] != y_combo:
                                razniza = max([y_combo, pos[1]]) - min([y_combo, pos[1]])
                                status_combo = False
                                sp = []
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
                                        print(0)
                                        i[2](fps_volt)
                                    elif i[1] == 'Действие назад':
                                        print(1)
                                        if len(list_action) != 0:
                                            print(list_action)
                                            elem = list_action.pop()
                                            if elem:
                                                if len(elem) > 2 and type(elem[-2]) == str:
                                                    print(1231234234345456567678678)
                                                    object = elem[2](all_sprites, elem[-2])
                                                    object.move([elem[0], elem[1]])
                                                    object.stop(elem[0], elem[1])
                                                    list_action[elem[-1]] = [elem[0], elem[1]]
                                                    all_sprites.remove(object)
                                                    elem[3].add(object)
                                                elif len(elem) > 2 and type(elem[-3]) == str:
                                                    object = elem[2](all_sprites, elem[-3])
                                                    object.move([elem[0], elem[1]])
                                                    object.stop(elem[0], elem[1])
                                                    list_action[elem[-2]][elem[-1]] = [elem[0], elem[1]]
                                                    all_sprites.remove(object)
                                                    elem[3].add(object)
                                                elif len(elem) > 2:
                                                    print()
                                                    print(elem)
                                                    for i in elem:
                                                        truba.update(i, dell=True)
                                                        board.take_a_position([i[0], i[1], 0])
                                                else:
                                                    truba.update(elem, dell=True)
                                                    angle.update(elem, dell=True)
                                                    board.take_a_position([elem[0], elem[1], 0])
                                    elif i[1] == 'Удалить обьект':
                                        status_dell = True
                                        print(2)
                                    elif i[1] == 'Очистить поле':
                                        print(3)
                                        truba.update(clear=True)
                                        angle.update(clear=True)
                                        board.new_pole()
                                        list_action = []
                                        spisok_number_combo_in_list_action = []


                                else:
                                    if status is False:
                                        print(1231324)
                                        object = i[1](all_sprites)
                                        type_sprite = i[2]
                                        status_combo = False
                                        status = True
                                        status_dell = False

                if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and status_combo is False and status \
                        is False:
                    pos = board.get_cell(event.pos)
                    if pos:
                        x_combo = pos[0]
                        y_combo = pos[1]
                        status_combo = True
                if event.type == pygame.KEYUP and event.key == pygame.K_o and status and status_combo is False:
                    object.rotate(1)
                elif event.type == pygame.KEYUP and event.key == pygame.K_p and status and status_combo is False:
                    object.rotate(-1)

                if event.type == pygame.MOUSEMOTION and status:
                    print(event.pos)
                    if board.get_cell(event.pos):
                        pos = board.get_cell(event.pos)
                        object.move(pos)

            board.render(screen)
            nachalo.draw(screen)
            end.draw(screen)
            all_sprites.draw(screen)
            angle.draw(screen)
            truba.draw(screen)
            smesitel.draw(screen)
            pygame.display.flip()
