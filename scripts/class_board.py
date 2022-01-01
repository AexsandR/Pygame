import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.x = 0
        self.y = 0
        self.cell_size = 30

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
