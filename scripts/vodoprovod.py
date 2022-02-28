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


object = None

board = Board(20, 14, [7, 0], [6, 0])
board.set_view(0, 0, 32)
shag = 1

slovar_sprite = None
spisok_activ_elem = []

stop = False


def element(cord, fps, screen, clock, ventilator):
    global stop
    if fps > 5:
        while stop:
            ventilator.update(cord)
            ventilator.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        return True


def zapolnenie(fps, screen, clock, sp, spisok_activ_elem):
    global stop
    global fps_volt
    res = board.proverka()
    if res:
        stop = True
        for i in range(8):
            board.render(screen)
            sp[1].update()
            sp[2].draw(screen)
            sp[1].draw(screen)
            sp[0].draw(screen)
            sp[4].draw(screen)
            sp[3].draw(screen)
            sp[-2].draw(screen)
            pygame.display.flip()
            clock.tick(8)
        fps_amper = posledovatelnoe_connect_om(res, slovar_smesitel, fps)
        run = False
        for cord in res:
            tmp = (cord[0], cord[1])
            if tmp in slovar_smesitel:
                fps = fps_amper * slovar_smesitel[tmp][0]
            if tmp in spisok_activ_elem:
                r = threading.Thread(target=element, args=(cord, fps, screen, clock, sp[-2]))
                r.start()
            for i in range(9):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if 0 <= event.pos[0] <= 638 and 609 <= event.pos[1] <= 609 + \
                                110:
                            sp[4].update(faza_null=True)
                            sp[0].update(faza_null=True)
                            stop = False

                            run = True
                            break
                if run:
                    break

                sp[-2].draw(screen)
                sp[0].update(cord)
                sp[4].update(cord)
                sp[0].draw(screen)
                sp[4].draw(screen)
                sp[3].draw(screen)
                pygame.display.flip()
                clock.tick(fps_amper)


def proverka_sp(pos, sp, all_sprites, type_sprite, setting_shag, list_action, spisok_activ_elem):
    global status
    global shag
    if object.proverka(sp):
        try:
            board.take_a_position([pos[0], pos[1], object.get_position()])
        except Exception as er:
            board.take_a_position([pos[0], pos[1], object.get_position()])
            object.stop(pos[0], pos[1])
            list_action.append([pos[0], pos[1]])
            all_sprites.remove(object)
            type_sprite.add(object)
            return False
        else:
            object.stop(pos[0], pos[1])
            list_action.append([pos[0], pos[1]])
            all_sprites.remove(object)
            type_sprite.add(object)
            if type_sprite == sp[3]:
                if slovar_sprite['smesitel']:
                    ...
                else:
                    slovar_sprite['smesitel'] = []
                slovar_sprite['smesitel'].append([pos[0], pos[1]])
                slovar_smesitel[(pos[0], pos[1])] = [0, shag]
                setting_shag = False
            if type_sprite == sp[-2]:
                spisok_activ_elem.append(pos)
                if slovar_sprite['ventilator']:
                    ...
                else:
                    slovar_sprite['ventilator'] = []
                slovar_sprite['ventilator'].append([pos[0], pos[1]])
            if type_sprite == sp[-3]:
                if slovar_sprite['angle']:
                    ...
                else:
                    slovar_sprite['angle'] = []
                slovar_sprite['angle'].append([pos[0], pos[1]])
            if type_sprite == sp[0]:

                if slovar_sprite['truba']:
                    ...
                else:
                    slovar_sprite['truba'] = []
                slovar_sprite['truba'].append([pos[0], pos[1]])

            return [False, setting_shag, list_action, spisok_activ_elem, slovar_sprite]
    else:
        return [True, setting_shag, list_action, spisok_activ_elem, slovar_sprite]


def proverka_combo(x, y, sp, all_sprites):
    global object
    if object.proverka(sp):
        try:
            board.take_a_position([x, y, object.get_position()])
        except Exception as er:
            board.take_a_position([x, y, object.get_position()])
            object.stop(x, y)
            all_sprites.remove(object)
            sp[0].add(object)
        else:
            object.stop(x, y)
            all_sprites.remove(object)
            sp[0].add(object)
            if slovar_sprite['truba']:
                ...
            else:
                slovar_sprite['truba'] = []
            slovar_sprite['truba'].append([x, y])
            return True, slovar_sprite
    else:
        object.kill()
        return False, slovar_sprite


def start(screen):
    global slovar_smesitel
    global object
    global stop
    global slovar_sprite
    clock = pygame.time.Clock()
    nachalo = pygame.sprite.Group()
    truba = pygame.sprite.Group()
    end = pygame.sprite.Group()
    smesitel = pygame.sprite.Group()
    angle = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    ventilator = pygame.sprite.Group()
    troinik = pygame.sprite.Group()
    s = board.load_save([truba, angle, ventilator, smesitel])
    slovar_smesitel = {}
    truba = s[0]
    angle = s[1]
    ventilator = s[2]
    smesitel = s[3]
    slovar_smesitel = s[4]
    spisok_activ_elem = s[5]
    slovar_sprite = s[6]
    list_action = s[7]


    status_combo = False

    fon = pygame.transform.scale(load_image('фон_с_кнопками.png'), (1280, 720))
    SPISOK_BUTTON = [[[641, 1, 318, 159], 'Действие назад', None], [[960, 1, 319, 159], 'Сохранить', None],
                     [[641, 161, 319, 159], 'Очистить поле', None], [[960, 161, 319, 159], 'Удалить обьект', None],
                     [[640, 321, 640, 93], 'Заполнение', zapolnenie],
                     [[640, 411, 190, 32], Ventilator, ventilator, None],
                     [[831, 418, 113, 32], Truba, truba, None],
                     [[944, 418, 176, 32], Smesitel, smesitel, None], [[1121, 418, 159, 40], Angle, angle, None],
                     [[1, 448, 319, 112], 'повернуть против часовой стрелке', None],
                     [[320, 448, 319, 112], 'по часовой стрелке', None], [[0, 609, 638, 110], 'стоп', None]]

    Nachalo(nachalo, 6)
    End(end, 1, 8)
    setting_shag = False
    x_combo = None
    y_combo = None
    status_dell = False
    all_sprites = pygame.sprite.Group()
    spisok_number_combo_in_list_action = []
    shag = 1
    running = True
    status = False

    while running:
        screen.fill((54, 54, 54))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                        s = proverka_sp(pos, [truba, nachalo, end, smesitel, angle,
                                              ventilator, troinik], all_sprites,
                                        type_sprite, setting_shag, list_action, spisok_activ_elem)

                        status = s[0]
                        setting_shag = s[1]
                        list_action = s[2]
                        spisok_activ_elem = s[3]
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
                            if len_truba > len(truba):
                                pos.append(truba)
                                pos.append(Truba)
                                slovar_sprite['truba'].remove([pos[0], pos[1]])
                                pos.append(board.to_give_position([pos[0], pos[1]]))
                            elif len_ventilator > len(ventilator):
                                pos.append(ventilator)
                                pos.append(Ventilator)
                                spisok_activ_elem.remove((pos[0], pos[1]))
                                slovar_sprite['ventilator'].remove([pos[0], pos[1]])
                                pos.append(board.to_give_position([pos[0], pos[1]]))
                            elif len_angle > len(angle):
                                pos.append(angle)
                                pos.append(Angle)
                                pos.append(board.to_give_position((pos[0], pos[1])))
                                slovar_sprite['angle'].remove([pos[0], pos[1]])
                            elif len_smesitel > len(smesitel):
                                pos.append(smesitel)
                                pos.append(Smesitel)
                                slovar_sprite['smesitel'].remove([pos[0], pos[1]])
                                pos.append(slovar_smesitel[(pos[0], pos[1])])
                                slovar_smesitel.pop((pos[0], pos[1]))
                                pos.append(board.to_give_position((pos[0], pos[1])))

                            pos.append(res)
                            list_action.append(pos)

                            board.take_a_position([pos[0], pos[1], 0])
                        else:
                            for i in spisok_number_combo_in_list_action:
                                if pos in list_action[i]:
                                    truba.update(pos, dell=True)
                                    res = list_action[i].index(pos)
                                    list_action[i][res] = None
                                    slovar_sprite['truba'].remove([pos[0], pos[1]])
                                    pos.append(truba)
                                    pos.append(Truba)

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
                                res, slovar_sprite = proverka_combo(x_combo, min([y_combo, pos[1]]) + i,
                                                     [truba, nachalo, end, smesitel, angle, ventilator, troinik],
                                                     all_sprites)
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
                                res, slovar_sprite = proverka_combo(max([x_combo, pos[0]]) - i, y_combo,
                                                     [truba, nachalo, end, smesitel, angle, ventilator, troinik],
                                                     all_sprites)
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
                                    i[2](fps_volt, screen, clock,
                                         [truba, nachalo, end, smesitel, angle, ventilator, troinik], spisok_activ_elem)
                                if i[1] == 'Сохранить':
                                    tmp = []
                                    for i in list_action:
                                        if isinstance(i, list):
                                            if len(i) == 2 and isinstance(i[0], int):
                                                tmp.append(i)
                                            else:
                                                if len(i) >= 2 and isinstance(i[0], list):
                                                    for j in i:
                                                        if isinstance(j, list):
                                                            tmp.append(j)

                                    board.save(slovar_sprite, spisok_activ_elem, slovar_smesitel, tmp)

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
                                            if len(elem) > 2 and isinstance(elem[0],list):
                                                    for j in elem:
                                                        truba.update(j, dell=True)
                                            elif len(elem) > 2:
                                                if elem[2] == truba:
                                                    slovar_sprite['truba'].append([elem[0], elem[1]])
                                                    if len(elem) == 6:
                                                        object = elem[3](all_sprites, elem[-2])
                                                        object.move([elem[0], elem[1]])
                                                        object.stop(elem[0], elem[1])
                                                        list_action[elem[-1]] = [elem[0], elem[1]]
                                                        all_sprites.remove(object)
                                                        elem[2].add(object)
                                                    else:
                                                        object = elem[3](all_sprites, elem[-3])
                                                        object.move([elem[0], elem[1]])
                                                        object.stop(elem[0], elem[1])
                                                        list_action[elem[-2]][elem[-1]] = [elem[0], elem[1]]
                                                        all_sprites.remove(object)
                                                        elem[2].add(object)
                                                elif elem[2] == smesitel:
                                                    slovar_sprite['smesitel'].append([elem[0], elem[1]])
                                                    slovar_smesitel[(elem[0], elem[1])] = elem[-3]
                                                    object = elem[3](all_sprites, elem[4])
                                                    object.move([elem[0], elem[1]])
                                                    object.stop(elem[0], elem[1])
                                                    list_action[elem[-1]] = [elem[0], elem[1]]
                                                    all_sprites.remove(object)
                                                    elem[2].add(object)
                                                else:
                                                    if elem[2] == angle:
                                                        slovar_sprite['angle'].append([elem[0], elem[1]])
                                                    elif elem[2] == ventilator:
                                                        slovar_sprite['ventilator'].append([elem[0], elem[1]])
                                                        spisok_activ_elem.append([elem[0], elem[1]])
                                                    object = elem[3](all_sprites, elem[4])
                                                    object.move([elem[0], elem[1]])
                                                    object.stop(elem[0], elem[1])
                                                    list_action[elem[5]] = [elem[0], elem[1]]
                                                    all_sprites.remove(object)
                                                    elem[2].add(object)
                                            else:
                                                len_truba = len(truba)
                                                len_angle = len(angle)
                                                len_smesitel = len(smesitel)
                                                len_ventilator = len(ventilator)
                                                truba.update(elem, dell=True)
                                                angle.update(elem, dell=True)
                                                smesitel.update(elem, dell=True)
                                                ventilator.update(elem, dell=True)
                                                if len_truba > len(truba):
                                                    slovar_sprite['truba'].remove([elem[0], elem[1]])
                                                elif len_angle > len(angle):
                                                    slovar_sprite['angle'].remove([elem[0], elem[1]])
                                                elif len_smesitel > len(smesitel):
                                                    slovar_sprite['smesitel'].remove([elem[0], elem[1]])
                                                    slovar_smesitel.pop((elem[0], elem[1]))
                                                elif len_ventilator > len(ventilator):
                                                    slovar_sprite['ventilator'].remove([elem[0], elem[1]])
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
                                    slovar_smesitel = {}
                                    slovar_sprite = {"truba": [],
                                                     "smesitel": [],
                                                     "angle": [],
                                                     "ventilator": [],
                                                     "troinik": []}
                                    spisok_number_combo_in_list_action = []
                            else:
                                if status is False and stop is False:
                                    object = i[1](all_sprites)
                                    type_sprite = i[2]
                                    object.get_sprite(type_sprite)
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

    return True
