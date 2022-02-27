import pygame
import json


class Board:
    # создание поля
    def __init__(self, width, height, end, nachalo):
        self.width = width
        self.height = height
        self.board = [["0"] * width for _ in range(height)]
        self.board[nachalo[0]][nachalo[1]] = '-'
        self.board[end[0]][end[1]] = 'end'
        # значения по умолчанию
        self.x = 0
        self.y = 0
        self.cell_size = 30
        self.p_x = nachalo[1]
        self.p_y = nachalo[0]

    def take_a_position(self, pos):
        x = pos[0]
        y = pos[1]
        position = pos[2]
        self.board[y][x] = position

    def to_give_position(self, pos):
        x = pos[0]
        y = pos[1]
        return self.board[y][x]
    def give_mat(self, sp):
        self.board = sp

    def save(self, spisok_sprite, spisok_activ_elem, slovar_smesitel, list_action):
        str_spisok = ''
        for rows in self.board:
            for i in range(len(rows) - 1):
                str_spisok += str(rows[i]) + ' '
            str_spisok += str(rows[-1]) + '\n'

        with open('save/save_marrix.txt', mode='w') as file:
            file.write(str_spisok)
            sl = {}
            for key, value in slovar_smesitel.items():
                sl[f"{key[0]} {key[1]}"] = value
            slovar_smesitel = sl
            slovar = {'sprite': spisok_sprite,
                      "spisok_activ_elem": spisok_activ_elem,
                      "slovar_smesitel": slovar_smesitel,
                      "list_action":list_action}
        with open('save/stuff.json', 'w') as file:

            json.dump(slovar, file)

    def load(self):
        with open('save/stuff.json', encoding='utf-8') as file:
            slovar = json.load(file)
        with open('save/save_marrix.txt', encoding='utf-8') as file:
            data = file.readlines()
        return [slovar, data]

    # настройка внешнего вида
    def set_view(self, x, y, cell_size):
        self.x += x
        self.y += y
        self.cell_size = cell_size

    def render(self, sc):
        x = self.x
        y = self.y
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(sc, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)
                x += self.cell_size
            x = self.x
            y += self.cell_size

    def new_pole(self):
        self.board = [[0] * self.width for _ in range(self.height)]
        self.board[6][0] = '-'
        self.board[7][0] = 'end'
        # значения по умолчанию
        self.x = 0
        self.y = 0

    def get_cell(self, Pos):
        x = self.x
        y = self.y
        for y1 in range(len(self.board)):
            for x1 in range(len(self.board[y1])):
                if y < Pos[1] < y + self.cell_size:
                    if x < Pos[0] < x + self.cell_size:
                        return (x1, y1)
                x += self.cell_size
            x = self.x
            y += self.cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

    def proverka(self):
        x = self.p_x
        y = self.p_y
        res = False
        spisok = []
        napr_x = 1
        napr_y = 0
        napravlenie = 'right'
        position = '-'

        while True:
            try:
                if isinstance(self.board[y][x], int):
                    break
                if position == '-' and self.board[y][x] == position:
                    spisok.append([x, y, napravlenie])
                    x += napr_x
                elif position == '|' and self.board[y][x] == position:
                    spisok.append([x, y, napravlenie])
                    y += napr_y
                elif self.board[y][x] == 'end':
                    res = True
                    break
                elif position == '-' and self.board[y][x] == '>|' and napravlenie == 'right':
                    if y == 13:
                        break
                    spisok.append([x, y, napravlenie, 'down'])
                    napravlenie = 'down'
                    napr_y = 1
                    y += napr_y
                    position = '|'
                elif position == '|' and self.board[y][x] == '>|' and napravlenie == 'up':
                    if x == 0:
                        break
                    napr_x = -1
                    spisok.append([x, y, napravlenie, 'left'])
                    x += napr_x
                    napravlenie = 'left'
                    position = '-'

                elif position == '-' and self.board[y][x] == '|>' and napravlenie == 'right':
                    if y == 0:
                        break
                    spisok.append([x, y, napravlenie, 'up'])
                    napr_y = -1
                    y += napr_y
                    napravlenie = 'up'
                    position = '|'
                elif position == '|' and self.board[y][x] == '|>' and napravlenie == 'down':
                    if x == 0:
                        break
                    spisok.append([x, y, napravlenie, 'left'])
                    napr_x = -1
                    x += napr_x
                    napravlenie = 'left'
                    position = '-'
                elif position == '|' and self.board[y][x] == '|-' and napravlenie == 'down':
                    if x == 19:
                        break
                    spisok.append([x, y, napravlenie, 'right'])
                    position = '-'
                    napravlenie = 'right'
                    napr_x = 1
                    x += napr_x
                elif position == '-' and self.board[y][x] == '|-' and napravlenie == 'left':
                    if y == 0:
                        break
                    spisok.append([x, y, napravlenie, 'up'])
                    position = '|'
                    napravlenie = 'up'
                    napr_y = -1
                    y += napr_y
                elif position == '|' and self.board[y][x] == '-|' and napravlenie == 'up':
                    if x == 19:
                        break
                    spisok.append([x, y, napravlenie, 'right'])
                    napravlenie = 'right'
                    napr_x = 1
                    x += napr_x
                    position = '-'
                elif position == '-' and self.board[y][x] == '-|' and napravlenie == 'left':
                    if x == 19:
                        break
                    spisok.append([x, y, napravlenie, 'down'])
                    napravlenie = 'down'
                    napr_y = 1
                    y += napr_y
                    position = '|'
                else:
                    break

            except Exception as err:

                break

        if res is True:
            return spisok
        else:
            return False



