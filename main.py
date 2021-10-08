import pygame
import sys
from typing import Union
from pygame import Surface, SurfaceType
import time


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


class Board:
    def __init__(self, screen: Union[Surface, SurfaceType]) -> None:
        self.screen = screen

    def draw(self) -> None:
        ww = CELL_WIDTH
        hh = CELL_HEIGHT
        for rows in range(1, GRID_ROWS):
            for columns in range(1, GRID_COLUMNS):
                xi = rows * ww
                xe = xi
                yi = 0
                ye = HEIGHT
                pygame.draw.line(self.screen,
                                 GREEN,
                                 (xi, yi),
                                 (xe, ye),
                                 10)
                xi = 0
                xe = WIDTH
                yi = columns * hh
                ye = yi
                pygame.draw.line(self.screen,
                                 WHITE,
                                 (xi, yi),
                                 (xe, ye),
                                 10)

    def fill_cell(self, row: int, column: int, color: tuple[int, int, int]) -> None:
        # 0 based row and columns please
        xi = column * CELL_WIDTH
        xe = (column+1) * CELL_WIDTH
        yi = row * CELL_HEIGHT
        ye = (row+1) * CELL_HEIGHT
        pygame.draw.rect(self.screen,
                         color,
                         ((xi, yi),
                          (xe, ye)),)


def main_loop():
    pygame.init()
    pygame.display.set_caption('Snake')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    board = Board(screen)
    running = True
    color_number = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(COLOR_PALETTE[color_number])
        board.draw()
        board.fill_cell(0, 0, BLACK)
        pygame.display.flip()
        color_number = (color_number + 1) % 4
        time.sleep(1.0)


if __name__ == "__main__":
    main_loop()
