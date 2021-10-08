import numpy as np
import random


BOARD_ROWS = 3
BOARD_COLUMNS = 3


class Board:
    def __init__(self):
        self.array = np.zeros((BOARD_ROWS, BOARD_COLUMNS), dtype=int)

    def find_empty_cell(self) -> tuple[int, int]:
        # find an empty cell and return its position as tuple of the form (row, column)
        valid_cell = False
        while not valid_cell:
            row = random.randrange(BOARD_ROWS)
            column = random.randrange(BOARD_COLUMNS)
            valid_cell = self.array[row][column] == 0
        return row, column


def main_loop():
    random.seed(a=0)
    board = Board()
    rr, cc =board.find_empty_cell()
    print(f'{rr},{cc}')
    board.array[rr][cc] = 1
    rr, cc = board.find_empty_cell()
    print(f'{rr},{cc}')

if __name__ == "__main__":
    main_loop()
