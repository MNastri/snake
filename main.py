import os  # TODO remove this.
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
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)

COLOR_PALETTE = {0: BLACK,
                 1: GREEN,
                 2: RED,
                 3: PURPLE,
                 4: WHITE}

GRID_ROWS = 3
GRID_COLUMNS = 3
CELL_WIDTH = WIDTH / GRID_COLUMNS
CELL_HEIGHT = HEIGHT / GRID_ROWS
LINE_WIDTH = 1


class Snake:
    def __init__(self, x: int, y: int) -> None:
        self.posx = x
        self.posy = y
        self.size = 1
        # direction = (x, y)
        #      ▲-y
        #      │
        # -x◄──┼──►+x
        #      │
        #      ▼+y
        self.direction = [1, 0]

    def move(self) -> bool:
        died = False
        self.posx += self.direction[0]
        self.posy += self.direction[1]
        if posx == GRID_COLUMNS or posy == GRID_ROWS:
            died = True
        return died

    def change_direction(self, d: int) -> None:
        # direction
        #      ▲1
        #      │
        #  2◄──┼──►0
        #      │
        #      ▼3
        if (d % 2 == 1 and self.direction[0] % 2 == 0) or (d % 2 == 0 and self.direction[0] % 2 == 1):
            self.direction[0] = 1 if d == 0 else -1 if d == 2 else 0
            self.direction[1] = 1 if d == 3 else -1 if d == 1 else 0


class Board:
    def __init__(self, screen: Union[Surface, SurfaceType]) -> None:
        self.screen = screen
        self.array = np.zeros((GRID_ROWS, GRID_COLUMNS), dtype=int)
        self.empty_cells = GRID_ROWS * GRID_COLUMNS
        self.is_full = False

    def __str__(self) -> str:
        return str(self.array)

    def fill_cell(self, row: int, column: int, color: tuple[int, int, int]) -> None:
        # 0 based row and columns please
        lw = LINE_WIDTH
        cw = CELL_WIDTH
        ch = CELL_HEIGHT

        xi = int(column * cw + lw)
        yi = int(row * ch + lw)
        ww = int(cw - 2*lw)
        hh = int(ch - 2*lw)
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
        if self.is_full:
            return -1, -1
        valid_cell = False
        row = column = None
        while not valid_cell:
            row = random.randrange(GRID_ROWS)
            column = random.randrange(GRID_COLUMNS)
            valid_cell = self.array[row][column] == 0
        return row, column

    def set_cell(self, value: int, row: int, column: int) -> None:
        # TODO maybe remove this. this checks if the cell is valid
        if row == -1:
            print("invalid cell")
            return
        self.empty_cells -= 1 if self.array[row][column] == 0 else 0
        if self.empty_cells == 0:
            self.is_full = True
        self.array[row][column] = value

    def replace_apple(self):
        rr, cc = self.find_empty_cell()
        self.set_cell(2, rr, cc)


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 32)  # TODO maybe remove this. This sets the screen position
        random.seed(a=0)  # TODO remove this. This removes randomness
        pygame.init()
        pygame.display.set_caption('Snake')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(PURPLE)
        self.board = Board(self.screen)
        self.snake = Snake(0, 0)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            self.board.set_cell(1, self.snake.posx, self.snake.posy)
            self.board.replace_apple()
            print(self.board)
            self.board.draw_cells()
            pygame.display.flip()
            time.sleep(3.0/6.0)  # TODO better interval management


def main_loop():
    game = Game()
    game.run()


if __name__ == "__main__":
    main_loop()
