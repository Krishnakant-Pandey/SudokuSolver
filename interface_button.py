import pygame as pg
import numpy as np
from gui_constants import *


class Button:
    def __init__(self, x, y, width, height, text_pos, text=None, color=(0, 0, 255),
                 function=None, params=None, font_size=40, ):

        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.topleft = self.pos

        self.color = color
        self.highlighted_color = 0, 0, 0

        self.function = function
        self.params = params

        self.text = text
        self.font_size = font_size
        self.text_pos = text_pos

        self.clicked = False

        self.WHITE = (255, 255, 255)
        self.font = pg.font.Font("sans.ttf", font_size)

    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.clicked = True
        else:
            self.clicked = False

    def draw(self, window):
        if self.clicked:
            self.image.fill(self.highlighted_color)
        else:
            self.image.fill(self.color)

        window.blit(self.image, self.pos)
        font = self.font.render(self.text, False, self.WHITE)

        window.blit(font, self.text_pos)

    def output(self):
        if self.clicked:
            if self.params is not None:
                self.function(self.params)
            else:
                self.function()
