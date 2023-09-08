from board import Board
from models import Position

import curses
from curses import window, wrapper
from typing import List, TYPE_CHECKING
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
        self.err = ""

        # curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        # curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        # curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

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
    
    def __pos2rc(self, pos: Position):
        pass
    
    def show(self, stdscr: window):
        """
        print the Game in the terminal
        """
        stdscr.addstr(f"  {TITLE_TEMPLATE}\n")
        row = 0
        out = ""
        while row<9:
            srow = {}
            for i in range(9):
                pos = self.__rc2pos(row, i)
                srow[LETTERS[i]] = self.get_svalue(pos)
            out += f"{row+1} "
            out += ROW_TEMPLATE.format_map(srow) + '\n'
            if (row+1) % 3 == 0 and row != 8:
                out += f" {HOR_SEP}\n"
            row += 1
        stdscr.addstr(out)
        if self.err != "":
            self.err += '\n'
            stdscr.addstr(self.err)

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

    def get_playing_range(self):
        if self.playing_board == 0:
            return "A-Z", "0-9"
        
        row, col = self.__pos2rc(Position(self.playing_board, 0, 0))
        row_range = f"{LETTERS[row]}-{LETTERS[row+2]}"
        col_range = f"{col}-{col+2}"
        return row_range, col_range

    def start_game(self, stdscr: window):
        """
        Kinda explains itself.
        """
        out = ""
        while True:
            stdscr.clear()
            self.show(stdscr)
            self.err = ""
            splayer = "O" if self.current_player else "X"
            letter_range, num_range = self.get_playing_range()
            stdscr.addstr(f"Possible range: [{letter_range}][{num_range}]\n")
            stdscr.addstr(f"{splayer}'s Turn: {out}")
            stdscr.refresh()
            inp = stdscr.getkey()
            if inp != '\n':
                out += inp
                continue
            else:
                turn = out
                out = ""
            try:
                print(f"TURN: {turn}")
                pos = self.__rc2pos(int(turn[1])-1, LETTERS.index(turn[0].lower()))
            except ValidationError as ve:
                self.err = f"Error: Incorrect Input. {ve}"
                continue
            ret, err = self.move(pos)
            if not ret:
                self.err = f"Error: {err}.\nTry again."
                continue
            # print(pos.json())
            if self.player_board().evaluate():
                break
            self.next_player()
            self.set_playing_board(pos.row, pos.column)
        print(f"Congrats!! {splayer} Won")
    
    
game_engine = Engine()
wrapper(game_engine.start_game)