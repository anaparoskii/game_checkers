import pygame
from .variables import WHITE, SQUARE_SIZE


class Piece(object):
    PADDING = 5

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        if self.color == WHITE:
            self.direction = 1
        else:
            self.direction = -1

        self.x = self.y = 0
        self.position()

    def position(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw_piece(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
