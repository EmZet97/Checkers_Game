import pygame
from UI import UI


class Text(UI.UI):
    def __init__(self, x, y, w = 0, h = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fun = None
        self.clickable = False
        self.color = (255, 255, 255)
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.clicked = lambda x, y: x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h



    def write(self, screen, text):
        textsurface = self.my_font.render(text, False, self.color)
        screen.blit(textsurface, (self.x, self.y))

    def make_clickable(self, fun):
        self.fun = fun
        self.clickable = True

    def check_if_clicked(self, x, y):
        if self.clicked(x, y):
            self.fun()

    def set_color(self, color):
        self.color = color
