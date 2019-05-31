import pygame


class Field:
    def __init__(self, size, x, y, *color):
        self.size = size
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.size, self.size))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def check_if_clicked(self, x, y):
        if self.x <= x and self.x + self.size >= x and self.y <= y and self.y + self.size >= y:
            return True
        return False
