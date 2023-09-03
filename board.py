import math
import re
import random
from typing import Tuple
import numpy as np

from models import Position

PATTERNS = ["111000000","000111000","000000111","100100100","010010010","001001001", "100010001", "001010100"]

class Board:
    def __init__(self) -> None:
        self.side = 3
        self.grid = [np.zeros((self.side,self.side), dtype=np.ubyte) for _ in range(9)]
        self.__current_player = 0
        self.active_board = 0
        self.won_boards = []
    
    def show(self):
        """
        return a string representation of the board
        """
        s_grid = []
        for board in self.grid:
            sb = ""
            for row in board:
                for col in row:
                    sb += str(col)
            s_grid.append(sb)
        return s_grid
    
    def get_value(self, pos: Position):
        self.grid[pos.board-1][pos.row-1][pos.column-1]
    
    def push(self, pos: Position) -> bool:
        self.grid[pos.board-1][pos.row-1][pos.column-1] = 1

    def evaluate_board(self, n: int):
        """
        Evaluate if player won in current board
        """
        sboard = "".join([str(col) for row in self.grid[n-1] for col in row])        

        if sboard in PATTERNS:
            self.won_boards.append(n-1)
            print(f"Player won in Board {n-1}")
        
        return sboard in PATTERNS

    def evaluate(self):
        """
        Evaluate if player won the game
        """
        sgrid = "".join(["1" if i in self.won_boards else "0" for i in range(9)])
        return sgrid in PATTERNS