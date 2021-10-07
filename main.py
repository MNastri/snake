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
    def __init__(self, screen: Union[Surface, SurfaceType]):
        self.screen = screen

    def draw(self):
        ww = CELL_WIDTH
        hh = CELL_HEIGHT
        for rows in range(1, GRID_ROWS):
            for columns in range(1, GRID_COLUMNS):
                pygame.draw.line(self.screen,
                                 GREEN,
                                 (rows * ww, 0),
                                 (rows * ww, HEIGHT),
                                 10)
                pygame.draw.line(self.screen,
                                 WHITE,
                                 (0, columns * hh),
                                 (WIDTH, columns * hh),
                                 10)



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
        pygame.display.flip()
        color_number = (color_number + 1) % 4
        time.sleep(1.0)


if __name__ == "__main__":
    main_loop()
