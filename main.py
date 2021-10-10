import pygame
import sys
from typing import Union
from pygame import Surface, SurfaceType
# from numpy import ndarray
import time
import numpy as np
import random


WIDTH = 600
HEIGHT = 600

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

COLOR_PALETTE = {0: BLACK,
                 1: GREEN,
                 2: RED,
                 3: WHITE}

GRID_ROWS = 3
GRID_COLUMNS = 3
CELL_WIDTH = WIDTH / GRID_COLUMNS
CELL_HEIGHT = HEIGHT / GRID_ROWS
LINE_WIDTH = 1


class Board:
    def __init__(self, screen: Union[Surface, SurfaceType]) -> None:
        self.screen = screen
        self.array = np.zeros((GRID_ROWS, GRID_COLUMNS), dtype=int)
        self.empty_cells = GRID_ROWS * GRID_COLUMNS

    def __str__(self) -> str:
        return str(self.array)

    def draw_grid(self) -> None:
        # TODO remove this method. a grid is not necessary if you fill the cells correctly
        ww = CELL_WIDTH
        hh = CELL_HEIGHT
        purple_color = (151, 119, 161)
        for rows in range(0, GRID_ROWS+1):
            for columns in range(0, GRID_COLUMNS+1):
                xi = rows * ww
                yi = 0
                xe = xi
                ye = HEIGHT
                pygame.draw.line(self.screen, purple_color, (xi, yi), (xe, ye), LINE_WIDTH)
                pygame.display.flip()
                time.sleep(0.16/9)
                xi = 0
                yi = columns * hh
                xe = WIDTH
                ye = yi
                pygame.draw.line(self.screen, purple_color, (xi, yi), (xe, ye), LINE_WIDTH)
                pygame.display.flip()
                time.sleep(0.16/9)

    def fill_cell(self, row: int, column: int, color: tuple[int, int, int]) -> None:
        # 0 based row and columns please
        lw = LINE_WIDTH
        cw = CELL_WIDTH
        ch = CELL_HEIGHT

        xi = column * cw + lw
        yi = row * ch + lw
        ww = cw - 2*lw
        hh = ch - 2*lw
        pygame.draw.rect(self.screen,
                         color,
                         (xi, yi, ww, hh))

    def draw_cells(self):
        for rr in range(GRID_ROWS):
            for cc in range(GRID_COLUMNS):
                color_number = self.array[rr][cc]
                self.fill_cell(rr, cc, COLOR_PALETTE[color_number])

    def find_empty_cell(self) -> tuple[int, int]:
        # find an empty cell and return its position as tuple or an error code
        if not self.empty_cells:
            return -1, -1
        valid_cell = False
        row = column = None
        while not valid_cell:
            row = random.randrange(GRID_ROWS)
            column = random.randrange(GRID_COLUMNS)
            valid_cell = self.array[row][column] == 0
        return row, column

    def set_cell(self, value: int, row: int, column: int) -> None:
        self.empty_cells -= 1 if self.array[row][column] == 0 else 0
        self.array[row][column] = value


def main_loop():
    pygame.init()
    pygame.display.set_caption('Snake')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BLACK)
    board = Board(screen)

    random.seed(a=0)  # removes randomness

    running = True
    # color_number = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        board.draw_grid()
        rr, cc = board.find_empty_cell()
        board.set_cell(2, rr, cc)
        print(board)
        board.draw_cells()
        pygame.display.flip()
        time.sleep(0.66)


if __name__ == "__main__":
    main_loop()
