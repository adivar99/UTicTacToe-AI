from board import Board
from models import Position

from typing import List
from pydantic import ValidationError

# constants
LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
TITLE_TEMPLATE = "  A   B   C    D   E   F    G   H   I  "
ROW_TEMPLATE = "  {a} | {b} | {c} || {d} | {e} | {f} || {g} | {h} | {i}  "
HOR_SEP = "="*39

class Engine:
    def __init__(self) -> None:
        self.x_board = Board()
        self.o_board = Board()
        self.current_player = 0
        self.playing_board = 0

    def sgrid(self) -> List[str]:
        """
        Get values of all grids in game
        """
        sgame = []
        for i in range(9):
            temp = []
            for j in range(9):
                if self.x_board.show()[i][j] == "1":
                    temp.append("X")
                elif self.o_board.show()[i][j] == "1":
                    temp.append("O")
                else:
                    temp.append(" ")
            sgame.append(temp)
        return sgame
    
    def get_svalue(self, pos: Position):
        """
        Returns value in position
        """
        board = self.sgrid()[pos.board-1]
        ind = (pos.row-1)*3 + (pos.column-1)
        return board[ind]
    
    def __rc2pos(self, row, col):
        """
        Converts row and columns to board, row, column
        """
        r = row % 3
        c = col % 3
        b = col // 3 + 3*(row // 3)
        pos = Position(
            board=b + 1,
            row=r+1,
            column=c+1
        )
        return pos
    
    def show(self):
        """
        print the Game in the terminal
        """
        sgrid = self.sgrid()
        print(" ",TITLE_TEMPLATE)
        row = 0
        while row<9:
            srow = {}
            for i in range(9):
                pos = self.__rc2pos(row, i)
                srow[LETTERS[i]] = self.get_svalue(pos)
            print(row+1, end=" ")
            print(ROW_TEMPLATE.format_map(srow))
            if (row+1) % 3 == 0 and row != 8:
                print(" ", HOR_SEP)
            row += 1

    def next_player(self):
        """
        Set current player to next player
        """
        self.current_player = (self.current_player+1)%2

    def player_board(self):
        """
        Get the board of the current player
        """
        return self.o_board if self.current_player else self.x_board
     
    def other_board(self):
        """
        Get the board of the player not currently playing
        """
        return self.x_board if self.current_player else self.o_board

    def move(self, pos: Position):
        """
        validate the move and then add the move
        TODO: add more validation
        """
        if self.playing_board !=0 and self.playing_board+1 != pos.board:
            return False, "Incorrect move. Please play in active board"
        
        if self.other_board().get_value(pos) == 1:
            return False, "Occupied position. Please choose another."
        
        if pos.board in self.player_board().won_boards or pos.board in self.other_board().won_boards:
            return False, "This board is already won. Please choose another."
        pb = self.player_board()
        pb.push(pos)
        pb.evaluate_board(pos.board)
        return True, ""
    
    def set_playing_board(self, row, col):
        """
        Set the active board after a move
        """
        self.playing_board = 3*(row-1) + (col-1)
        if self.playing_board in self.x_board.won_boards or self.playing_board in self.o_board.won_boards:
            self.playing_board = 0
        print("Playing board: ", self.playing_board)

    def start_game(self):
        """
        Kinda explains itself.
        """
        while True:
            self.show()
            splayer = "O" if self.current_player else "X"
            turn = input(f"{splayer}'s Turn: ")
            try:
                pos = self.__rc2pos(int(turn[1])-1, LETTERS.index(turn[0].lower()))
            except ValidationError as ve:
                print(f"Error: Incorrect Input. {ve}")
                continue
            ret, err = self.move(pos)
            if not ret:
                print(f"Error: {err}.\nTry again.")
                continue
            print(pos.json())
            if self.player_board().evaluate():
                break
            self.next_player()
            self.set_playing_board(pos.row, pos.column)
        print(f"Congrats!! {splayer} Won")
    
    
game_engine = Engine()
game_engine.start_game()