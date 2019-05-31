import pygame
from Field import Field

class Board:
    _colors = [(255, 255, 241), (153, 102, 51)]

    def __init__(self, size, x, y, field_size):
        self.size = size
        self.fields = []
        self.pawns = []
        self.x = x
        self.y = y
        self.field_size = field_size
        self.create()

    def create(self):
        for i in range(self.size):
            self.fields.append([])
            self.pawns.append([])
            for j in range(self.size):
                x = self.x + j * self.field_size
                y = self.y + i * self.field_size
                self.fields[i].append(Field(self.field_size, x, y, self._colors[(i + j) % 2]))
                self.pawns[i].append(None)
               # print("i: ", i , " j: ", j)
        #print(self.pola)

    def draw(self, screen):
        # draw 2D array of fields
        for i in range(self.size):
            for j in range(self.size):
                self.fields[i][j].draw(screen)



