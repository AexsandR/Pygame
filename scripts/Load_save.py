from pprint import pprint

import null as null
import pygame

from sprite_truba import *
from sprite_smesitel import Smesitel
from sprite_ventelator import Ventilator
from sprite_angle import Angle


def load_save(ex, sp_sprite):
    slovar, spisok = ex.load()
    all_sprites = pygame.sprite.Group()
    matrix = []
    sp = []
    for i in spisok:
        matrix.append(i[:-1].split())
    ex.give_mat(matrix)
    slovar_smesitel = {}
    for key, value in slovar['slovar_smesitel'].items():
        q = key.split()
        slovar_smesitel[(int(q[0]), int(q[1]))] = value
    for key, value in slovar['sprite'].items():
        if value:
            ...
        else:
            value = []
        for i in value:

            sprite = None
            cls = None
            q = True
            if key == 'truba':
                sprite = sp_sprite[0]
                cls = Truba
            elif key == 'angle':
                sprite = sp_sprite[1]
                cls = Angle
            elif key == 'ventilator':
                sprite = sp_sprite[2]
                q = True
                cls = Ventilator
            elif key == 'smesitel':
                sprite = sp_sprite[3]
                cls = Smesitel

            for elem in value:
                try:
                    if q:
                        sp.append((elem[0],elem[1]))
                except Exception:
                    sp = []
                object = cls(sprite, pos_in_mas=matrix[elem[1]][elem[0]])
                object.move(elem)
                object.stop(elem[0], elem[1])
    return [sp_sprite[0], sp_sprite[1], sp_sprite[2], sp_sprite[3], slovar_smesitel, sp,
            slovar['sprite'], slovar['list_action']]
