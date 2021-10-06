import pygame
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


def main_loop():
    pygame.init()
    pygame.display.set_caption('Snake')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    running = True
    color_number = 0
    while running:
        for event in pygame.event.get():
            pass
        screen.fill(COLOR_PALETTE[color_number])
        pygame.display.flip()
        color_number = (color_number + 1) % 4
        time.sleep(3.0)


if __name__ == "__main__":
    main_loop()
