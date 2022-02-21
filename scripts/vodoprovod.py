from class_board import Board
from sprite_nachlo import Nachalo
from sprite_end import End
from sprite_truba import *
from sprite_angle import Angle
import sys
from Posledovatelnoe_connect import posledovatelnoe_connect_om
from sprite_smesitel import Smesitel
from sprite_ventelator import Ventilator
import threading
from sprite_three import Three
from Load_save import load_save


def element(cord, fps):
    global stop
    print(fps)
    if fps > 5:
        while stop:
            ventilator.update(cord)
            ventilator.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        return True


def zapolnenie(fps):
    print(fps)
    global stop
    global fps_volt
    res = board.proverka()
    if res:
        stop = True
        print(
            '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        for i in range(8):
            board.render(screen)
            nachalo.update()
            end.draw(screen)
            nachalo.draw(screen)
            truba.draw(screen)
            angle.draw(screen)
            smesitel.draw(screen)
            ventilator.draw(screen)
            pygame.display.flip()
            clock.tick(8)
        fps_amper = posledovatelnoe_connect_om(res, slovar_smesitel, fps_volt)
        print(fps_amper)
        run = False
        for cord in res:
            tmp = (cord[0], cord[1])
            if tmp in slovar_smesitel:
                fps_volt = fps_amper * slovar_smesitel[tmp][0]
            if tmp in spisok_activ_elem:
                r = threading.Thread(target=element, args=(cord, fps_volt))
                r.start()
            for i in range(9):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if 0 <= event.pos[0] <= 638 and 609 <= event.pos[1] <= 609 + \
                                110:
                            angle.update(faza_null=True)
                            truba.update(faza_null=True)
                            stop = False

                            run = True
                            break
                if run:
                    break
                ventilator.draw(screen)
                truba.update(cord)
                angle.update(cord)
                truba.draw(screen)
                angle.draw(screen)
                smesitel.draw(screen)
                pygame.display.flip()
                clock.tick(fps_amper)


def proverka_sp(pos, type_sprite):
    global status
    global shag
    global setting_shag
    if object.proverka([truba, nachalo, end, smesitel, angle, ventilator]):
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
                slovar_sprite['smesitel'].append(pos)
                slovar_smesitel[(pos[0], pos[1])] = [0, shag]
                setting_shag = False
            if type_sprite == ventilator:
                spisok_activ_elem.append(pos)
                slovar_sprite['ventilator'].append(pos)
                print(spisok_activ_elem)
            if type_sprite == angle:
                slovar_sprite['angle'].append(pos)
            if type_sprite == truba:
                slovar_sprite['truba'].append(pos)
            if type_sprite == troinik:
                slovar_sprite['troinik'].append(pos)
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
            slovar_sprite['truba'].append([x, y])
            return True
    else:
        object.kill()


if __name__ != '__main__':
    stop = False
    board = Board(20, 14,[7,0],[6,0])
    board.set_view(0, 0, 32)

    pygame.init()
    shag = 1
    screen = pygame.display.set_mode((1280, 720))
    fon = pygame.transform.scale(load_image('фон_с_кнопками.png'), (1280, 720))
    clock = pygame.time.Clock()
    nachalo = pygame.sprite.Group()
    truba = pygame.sprite.Group()
    end = pygame.sprite.Group()
    smesitel = pygame.sprite.Group()
    angle = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    ventilator = pygame.sprite.Group()
    troinik = pygame.sprite.Group()
    slovar_sprite = {"truba": [],
                     "smesitel": [],
                     "angle": [],
                     "ventilator": [],
                     "troinik": []}
    spisok_activ_elem = []
    status_combo = False
    list_action = []
    s = load_save(board, [truba, angle, ventilator, smesitel])
    print(s)
    slovar_smesitel = {}
    truba = s[0]
    angle = s[1]
    ventilator = s[2]
    smesitel = s[3]
    slovar_smesitel = s[4]
    spisok_activ_elem = s[5]
    SPISOK_BUTTON = [[[641, 1, 318, 159], 'Действие назад', None], [[960, 1, 319, 159], 'Сохранить', None],
                     [[641, 161, 319, 159], 'Очистить поле', None], [[960, 161, 319, 159], 'Удалить обьект', None],
                     [[640, 321, 640, 93], 'Заполнение', zapolnenie],
                     [[640, 411, 190, 32], Ventilator, ventilator, None],
                     [[831, 418, 113, 32], Truba, truba, None],
                     [[640, 448, 209, 32], Three, troinik, None],
                     [[944, 418, 176, 32], Smesitel, smesitel, None], [[1121, 418, 159, 40], Angle, angle, None],
                     [[1, 448, 319, 112], 'повернуть против часовой стрелке', None],
                     [[320, 448, 319, 112], 'по часовой стрелке', None], [[0, 609, 638, 110], 'стоп', None]]

    Nachalo(nachalo,6)
    End(end, 1, 8)
    fps_volt = 120
    fps_amper = fps_volt
    setting_shag = False
    x_combo = None
    y_combo = None
    status_dell = False
    FPS = 20
    x = 0
    y = 0
    all_sprites = pygame.sprite.Group()
    spisok_number_combo_in_list_action = []
    if 1 == 1:
        running = True
        status = False

        while running:
            screen.fill((54, 54, 54))
            screen.blit(fon, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(124134146)
                    running = False
                if event.type == pygame.QUIT:
                    stop = False
                    running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = board.get_cell(event.pos)
                    if pos and status_dell is False:

                        if (pos[0], pos[1]) in slovar_smesitel:
                            slovar_smesitel[(pos[0], pos[1])][0] = (slovar_smesitel[(pos[0], pos[1])][0] +
                                                                    slovar_smesitel[(pos[0], pos[1])][1]) % (
                                                                           5 * slovar_smesitel[(pos[0], pos[1])][1])
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
                                len_smesitel = len(smesitel)
                                len_ventilator = len(ventilator)
                                truba.update(pos, dell=True)
                                ventilator.update(pos, dell=True)
                                angle.update(pos, dell=True)
                                smesitel.update(pos, dell=True)

                                res = list_action.index(pos)
                                list_action[res] = None
                                if len_truba - 1 == len(truba):
                                    pos.append(Truba)
                                    pos.append(truba)
                                    pos.append(board.to_give_position([pos[0], pos[1]]))
                                elif len_ventilator - 1 == len(ventilator):
                                    pos.append(Ventilator)
                                    pos.append(ventilator)
                                    spisok_activ_elem.remove((pos[0], pos[1]))
                                    pos.append(board.to_give_position([pos[0], pos[1]]))
                                elif len_angle - 1 == len(angle):
                                    pos.append(Angle)
                                    pos.append(angle)
                                    pos.append(board.to_give_position([pos[0], pos[1]]))
                                elif len_smesitel - 1 == len(smesitel):
                                    pos.append(Smesitel)
                                    pos.append(smesitel)
                                    slovar_smesitel[(pos[0], pos[1])][0] = 0
                                    pos.append(slovar_smesitel[(pos[0], pos[1])])
                                    pos.append(board.to_give_position([pos[0], pos[1]]))

                                pos.append(res)
                                list_action.append(pos)

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

                        for i in SPISOK_BUTTON:
                            if i[0][0] <= event.pos[0] <= i[0][0] + i[0][2] and i[0][1] <= event.pos[1] <= i[0][1] + \
                                    i[0][3]:
                                if len(i) == 3:
                                    if i[1] == 'Заполнение' and stop is False:
                                        fps_volt = 120
                                        i[2](fps_volt)
                                    if i[1] == 'Сохранить':
                                        fps_volt = 120
                                        board.save(slovar_sprite, spisok_activ_elem, slovar_smesitel)
                                    elif i[
                                        1] == 'повернуть против часовой стрелке' and status and status_combo \
                                            is False and stop is False:
                                        object.rotate(1)
                                    elif i[
                                        1] == 'по часовой стрелке' and status and status_combo is False and \
                                            stop is False:
                                        object.rotate(-1)
                                    elif i[1] == 'стоп':
                                        stop = False

                                        angle.update(faza_null=True)
                                        truba.update(faza_null=True)
                                        stop = False
                                    elif i[1] == 'Действие назад' and stop is False:
                                        status_dell = False

                                        if len(list_action) != 0:

                                            elem = list_action.pop()

                                            if elem:
                                                if len(elem) > 2 and type(elem[-2]) == str:
                                                    object = elem[2](all_sprites, elem[-2])
                                                    object.move([elem[0], elem[1]])
                                                    object.stop(elem[0], elem[1])
                                                    list_action[elem[-1]] = [elem[0], elem[1]]
                                                    all_sprites.remove(object)
                                                    elem[3].add(object)
                                                    if elem[3] == ventilator:
                                                        spisok_activ_elem.append((elem[0], elem[1]))
                                                    board.take_a_position([elem[0], elem[1], object.get_position()])
                                                elif len(elem) > 2 and type(elem[-3]) == str:

                                                    object = elem[2](all_sprites, elem[-3])
                                                    object.move([elem[0], elem[1]])
                                                    object.stop(elem[0], elem[1])
                                                    list_action[elem[-2]][elem[-1]] = [elem[0], elem[1]]
                                                    all_sprites.remove(object)
                                                    elem[3].add(object)

                                                    board.take_a_position([elem[0], elem[1], object.get_position()])
                                                elif len(elem) == 7 and type(elem[-2]) == str:
                                                    ...
                                                elif len(elem) > 2:

                                                    for i in elem:
                                                        truba.update(i, dell=True)
                                                else:
                                                    truba.update(elem, dell=True)
                                                    angle.update(elem, dell=True)
                                                    smesitel.update(elem, dell=True)
                                                    board.take_a_position([elem[0], elem[1], 0])
                                    elif i[1] == 'Удалить обьект' and stop is False:
                                        status_dell = True

                                    elif i[1] == 'Очистить поле' and stop is False:
                                        truba.update(clear=True)
                                        angle.update(clear=True)
                                        smesitel.update(clear=True)
                                        ventilator.update(clear=True)
                                        board.new_pole()
                                        list_action = []
                                        spisok_activ_elem = []
                                        spisok_number_combo_in_list_action = []
                                else:
                                    if status is False and stop is False:
                                        object = i[1](all_sprites)
                                        type_sprite = i[2]
                                        if type_sprite == smesitel:
                                            setting_shag = True
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

                if event.type == pygame.MOUSEMOTION and status:

                    if board.get_cell(event.pos):
                        pos = board.get_cell(event.pos)
                        object.move(pos)
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_UP] and shag != 100 and setting_shag:
                shag += 1
            if key_pressed[pygame.K_DOWN] and shag != 1 and setting_shag:
                shag -= 1
            if setting_shag:
                font = pygame.font.Font(None, 100)
                if shag < 10:
                    text = font.render(f"    шаг {shag} ом", True, (100, 255, 100))
                elif 9 < shag < 26:
                    text = font.render(f"  шаг {shag} ом", True, (100, 255, 100))
                screen.blit(text, (900, 660))
            board.render(screen)
            nachalo.draw(screen)
            end.draw(screen)
            all_sprites.draw(screen)
            angle.draw(screen)
            truba.draw(screen)
            smesitel.draw(screen)
            ventilator.draw(screen)
            troinik.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
