import numpy as np
import random
# from typing import Union


BOARD_ROWS = 3
BOARD_COLUMNS = 3


class Board:
    def __init__(self):
        self.array = np.zeros((BOARD_ROWS, BOARD_COLUMNS), dtype=int)
        self.empty_cells = BOARD_ROWS * BOARD_COLUMNS

    def find_empty_cell(self) -> tuple[int, int]:
        # find an empty cell and return its position as tuple or an error
        if not self.empty_cells:
            return -1, -1
        valid_cell = False
        row = column = None
        while not valid_cell:
            row = random.randrange(BOARD_ROWS)
            column = random.randrange(BOARD_COLUMNS)
            valid_cell = self.array[row][column] == 0
        return row, column

    def set_cell(self, value: int, row: int, column: int) -> None:
        self.empty_cells -= 1 if self.array[row][column] == 0 else 0
        self.array[row][column] = value


def main_loop():
    random.seed(a=0)
    board = Board()
    print(board.array)
    for _ in range(BOARD_ROWS * BOARD_COLUMNS+1):
        rr, cc = board.find_empty_cell()
        print(f'{rr},{cc}')
        board.set_cell(1, rr, cc)
        print(board.array)


if __name__ == "__main__":
    main_loop()
