import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board[0][0] = '-'
        self.board[0][width - 1] = 'end'
        # значения по умолчанию
        self.x = 0
        self.y = 0
        self.cell_size = 30

    def take_a_position(self, pos):
        x = pos[0]
        y = pos[1]
        position = pos[2]
        self.board[y][x] = position
        for i in self.board:
            print(i)

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
        print(cell)

    def proverka(self):
        x = 0
        y = 0
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
                    spisok.append([x, y, napravlenie,'left'])
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
                    spisok.append([x, y,napravlenie,'right'])
                    position = '-'
                    napravlenie = 'right'
                    napr_x = 1
                    x += napr_x
                elif position == '-' and self.board[y][x] == '|-' and napravlenie == 'left':
                    if y == 0:
                        break
                    spisok.append([x, y, napravlenie,'up'])
                    position = '|'
                    napravlenie = 'up'
                    napr_y = -1
                    y += napr_y
                elif  position == '|' and self.board[y][x] == '-|' and napravlenie == 'up':
                    if x == 19:
                        break
                    spisok.append([x, y, napravlenie,'right'])
                    napravlenie = 'right'
                    napr_x = 1
                    x += napr_x
                    position = '-'
                elif  position == '-' and self.board[y][x] == '-|' and napravlenie == 'left':
                    if x == 19:
                        break
                    spisok.append([x, y, napravlenie,'down'])
                    napravlenie = 'down'
                    napr_y = 1
                    y += napr_y
                    position = '|'
                else:
                    break

            except Exception as err:
                print(err)
                break
        print()
        print(spisok)
        if res is True:
            return spisok
        else:
            return False
