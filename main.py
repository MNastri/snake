import os  # TODO remove this.
import pygame
import sys
from typing import Union, List
position = List[int, int]
positions = List[position, ...]
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

# TENTATIVA...
class SnakeBody:
    def __init__(self, pos_x: int, pos_y: int):
        """ Constructor for SnakeBody. """
        self.pos_x = pos_x
        self.pos_y = pos_y


class Snake:
    """ Snake, snake, snake. """
    def __init__(self, x: int, y: int) -> None:
        """ Constructor for class Snake. """
        self.head_pos_x = x  # Column
        self.head_pos_y = y  # Row
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
        self.tail_pieces = [[None, None]]

    def check_if_died(self):
        """ Checks if snake died. """
        self.is_alive = False

        # Change to its next position
        # new_head_pos_x = self.head_pos_x + self.velocity[0]
        # new_head_pos_y = self.head_pos_y + self.velocity[1]

        # Check if hit the walls
        if self.head_pos_x == GRID_COLUMNS or \
           self.head_pos_y == GRID_ROWS or \
           self.head_pos_x == -1 or \
           self.head_pos_y == -1:
            return
        # TODO check collision with its tail
        head_piece = [self.head_pos_x, self.head_pos_y]  # TODO need to check if this is correct (i think so) or if the correct is [[head_x, head_y]]
        for tail_piece in self.tail_pieces:
            if head_piece == tail_piece:
                return

        # if didn't meet any death condition, it's alive
        self.is_alive = True

    def move(self) -> None:
        """ Move the snake. """
        self.head_pos_x += self.velocity[0]
        self.head_pos_y += self.velocity[1]
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
        self.change_velocity()

    def get_snake_pos(self):
        """ Returns an array with the snake pieces' position """
        head_piece = [self.head_pos_x, self.head_pos_y]
        snake_pieces = [head_piece]
        snake_pieces.extend(self.tail_pieces)
        print(f"snake_pieces={snake_pieces}")  # TODO removeeee
        return snake_pieces

    def add_tail_piece(self):
        """ Adds another tail piece into the snake. """
        pass



class Board:
    def __init__(self, screen: Union[Surface, SurfaceType]) -> None:
        self.screen = screen
        self.array = np.zeros((GRID_ROWS, GRID_COLUMNS), dtype=int)
        self.number_empty_cells = GRID_ROWS * GRID_COLUMNS
        self.is_full = False
        self.apple_pos = [None, None]

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

    def set_cell(self, value: int, cell_row: int, cell_column: int) -> None:
        self.number_empty_cells -= 1 if self.array[cell_row][cell_column] == 0 else 0
        if self.number_empty_cells == 0:
            self.is_full = True
        self.array[cell_row][cell_column] = value

    def replace_apple(self):
        rr, cc = self.find_empty_cell()
        self.apple_pos = [rr, cc]
        self.set_cell(2, rr, cc)

    def update_snake(self, snake_positions: positions) -> None:
        for rr in range(GRID_ROWS):
            for cc in range(GRID_COLUMNS):
                if self.array[rr][cc] == 1:
                    self.set_cell(0, rr, cc)

        for position in snake_positions:
            self.set_cell(1, position[0], position[1])


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
        self.board.set_cell(1, self.snake.head_pos_y, self.snake.head_pos_x)
        self.board.replace_apple()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            print(self.board)
            self.board.draw_cells()
            time.sleep(120.0/60.0)  # TODO better interval management
            self.snake.move()
            snake_positions = self.snake.get_snake_pos()

            self.board.update_snake(snake_positions)

            if not self.snake.is_alive:
                running = False
                time.sleep(3)
            pygame.display.flip()


def main_loop():
    game = Game()
    game.run()
    sys.exit()


if __name__ == "__main__":
    main_loop()
