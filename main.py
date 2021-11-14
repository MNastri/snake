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
    """ Snake, snake, snake. """
    def __init__(self, x: int, y: int) -> None:
        """ Constructor for class Snake. """
        self.pos_x = x  # Column
        self.pos_y = y  # Row
        # velocity = [x, y]
        #      ▲-y
        #      │
        # -x◄──┼──►+x
        #      │
        #      ▼+y
        self.velocity = [1, 0]  # ["going 1 right", "going 0 down"]
        # direction
        #      ▲1
        #      │
        #  2◄──┼──►0
        #      │
        #      ▼3
        self.direction = 0
        self.size = 1  # Todo probably should change this
        self.is_alive = True

    def check_if_died(self):
        """ Checks if snake died. """
        if self.pos_x == GRID_COLUMNS or self.pos_y == GRID_ROWS:
            self.is_alive = False
        # TODO improve
        pass

    def move(self) -> None:
        """ Move the snake. """
        self.pos_x += self.velocity[0]
        self.pos_y += self.velocity[1]
        self.check_if_died()

    def change_velocity(self):
        """ Change the snake's velocity. """
        # (1 if "going positive direction in x axis" else -1) * ("going right or left")
        self.velocity[0] = (1 if self.direction//2 == 0 else -1)*(self.direction % 2 == 0)

        # (1 if "going positive direction in y axis" else -1) * ("going up or down")
        self.velocity[1] = (1 if self.direction//2 == 1 else -1)*(self.direction % 2 == 1)

    def change_direction(self, new_direction: int) -> None:
        # new_direction
        #      ▲1
        #      │
        #  2◄──┼──►0
        #      │
        #      ▼3
        if (new_direction == 0 and self.direction == 2) or \
           (new_direction == 1 and self.direction == 3) or \
           (new_direction == 2 and self.direction == 0) or \
           (new_direction == 3 and self.direction == 1):
            return
        self.direction = new_direction


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

    def update_snake(self, row: int, column: int) -> None:
        for rr in range(GRID_ROWS):
            for cc in range(GRID_COLUMNS):
                if self.array[rr][cc] == 1:
                    self.set_cell(1, rr, cc)
        self.set_cell(1, row, column)


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
        self.board.set_cell(1, self.snake.pos_y, self.snake.pos_x)
        self.board.replace_apple()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            print(self.board)
            self.board.draw_cells()
            time.sleep(60.0/60.0)  # TODO better interval management
            self.snake.move()
            self.board.update_snake(self.snake.pos_y, self.snake.pos_x)
            # TODO fix this. crashes before showing the last snake position (0,2)
            if not self.snake.is_alive:
                running = False
                time.sleep(3)
            pygame.display.flip()


def main_loop():
    game = Game()
    game.run()


if __name__ == "__main__":
    main_loop()
