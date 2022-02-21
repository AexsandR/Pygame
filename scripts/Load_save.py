from pprint import pprint
import pygame


from sprite_truba import *
from sprite_smesitel import Smesitel
from sprite_ventelator import Ventilator
from sprite_angle import Angle


def load_save(ex, sp_sprite):
    slovar, spisok = ex.load()
    pprint(slovar)
    all_sprites = pygame.sprite.Group()
    matrix = []
    for i in spisok:
        matrix.append(i[:-1].split())
    ex.give_mat(matrix)

    for key, value in slovar['sprite'].items():
        for i in value:
            sprite = None
            cls = None
            if key == 'truba':
                sprite = sp_sprite[0]
                cls = Truba
            elif key == 'angle':
                sprite = sp_sprite[1]
                cls = Angle
            elif key == 'ventilator':
                sprite = sp_sprite[2]
                cls = Ventilator
            elif key == 'smesitel':
                sprite = sp_sprite[3]
                cls = Smesitel

            for elem in value:
                object = cls(sprite, pos_in_mas=matrix[elem[1]][elem[0]])
                object.move(elem)
                object.stop(elem[0], elem[1])
                pprint('lkbyf: ' + f'{elem}')
    return [sp_sprite[0], sp_sprite[1], sp_sprite[2], sp_sprite[3], slovar['sprite']['smesitel'], slovar['sprite'],
            ['list_action']]
