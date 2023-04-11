"""
Created by Avi Serebrenik
An adjustable tic-tac-toe game built with Python and Tkinter.
The base tic-tac-toe game was found in the following guide: https://realpython.com/tic-tac-toe-python/
"""

import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

"""Solves segmentation fault error that appeared"""
import faulthandler
faulthandler.enable()

class Player(NamedTuple):   #player class
    label: str  #store x or o
    color:str   #color for player indentification

class Move(NamedTuple):     #class for each move
    row:int     #coordinates of move
    col:int
    label:str = ""  #whether move is legal

BOARD_SIZE = 5
WIN_SIZE = 3
MAX_WIN = 10
MAX_SIZE = 20
DEFAULT_PLAYERS = (Player(label="X", color="blue"),
                   Player(label="O", color="green"))

def board_adjust(i):
    """Adjusts the global variable of Board Size"""
    global BOARD_SIZE
    BOARD_SIZE = i

def win_adjust(i):
    """Adjusts the global variable of Win Size"""
    global WIN_SIZE
    WIN_SIZE = i

class StartScreen(tk.Tk):
    """Creates the start screen before the game"""
    def __init__(self):
        super().__init__()                  #initialize parent class
        self.title("Mega Tic-Tac-Toe")      #title bar
        #self._create_menu()                #set up if menu needed
        self._create_display()
        self._create_screen()

    def _create_display(self):
        """Creates the base display frame"""
        display_frame = tk.Frame(master=self)       #frame object holds display, main window is parent
        display_frame.pack(fill=tk.X)               
        self.display = tk.Label(master=display_frame,   #creates display title
                                text="Mega Tic Tac Toe", 
                                font=font.Font(size=28, weight="bold"),
                                padx=100)
        self.display.pack()
    
    def _create_screen(self):
        """Creates the sliders and button in the start screen"""
        screen_frame = tk.Frame(master = self)    #create frame for board frame
        screen_frame.pack()
        size_scale = tk.Scale(master = screen_frame,    #scale for size adjustment
                              orient = "horizontal",
                              from_ = 2,
                              to=MAX_SIZE,
                              command= board_adjust)
        win_scale = tk.Scale(master = screen_frame,     #scale for win adjustment
                              orient = "horizontal",
                              from_ = 2,
                              to=MAX_WIN,
                              command= win_adjust)
        size_name = tk.Label(master = screen_frame,
                              text = "Board Size:")
        win_name = tk.Label(master = screen_frame,
                              text = "Win Size:")
        start_button = tk.Button(master = screen_frame, #button to start game
                                 text = "Start",
                                 command = self.destroy)
        size_name.grid(row = 1, column = 0, pady = 15)
        size_scale.grid(row = 1, column = 2, pady = 15)
        win_name.grid(row = 2, column = 0, padx = 10)
        win_scale.grid(row = 2, column = 2)
        start_button.grid(row = 3, column = 1, pady = 15)


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size = BOARD_SIZE, win_size = WIN_SIZE):
        self._players = cycle(players)  #cycles over player tuple
        self.board_size = board_size
        self.win_size = win_size    
        self.current_player = next(self._players)
        self.winner_combo=[]        #combo that defines winner
        self._current_moves = []    #list of player moves
        self._has_winner = False    #if win
        self._winning_combos = []   #list with combos that make a win
        self._setup_board()

    
    def _setup_board(self):
        self._current_moves = [[Move(row, col) for col in range(self.board_size)]
                               for row in range(self.board_size)]   #initial list of player moves
        self._winning_combos = self._get_winning_combos()
    
    def _get_winning_combos(self):
        """Returns an array of all possible winning combinations"""
        rows = []
        columns = []
        first_diagonal = [] #Diagonals with negative slope
        second_diagonal = [] #Diagonals with positive slope
        for i in range(self.board_size):        #rows
            for j in range(self.board_size-self.win_size+1):    #columns
                rows.append([])
                columns.append([])
                if i<self.board_size-self.win_size+1:
                    first_diagonal.append([])
                #second_diagonal.append([])
                for k in range(self.win_size):  #length of each win
                    rows[i*(self.board_size-self.win_size+1)+j].append((i, j+k))
                    columns[i*(self.board_size-self.win_size+1)+j].append((j+k, i))
                    if i<self.board_size-self.win_size+1:
                        first_diagonal[i*(self.board_size-self.win_size+1)+j].append((i+k,j+k))
        #second loop for second diagonal->easier to set up this way
        for i in range(self.win_size-1, self.board_size):       #rows
            for j in range(self.board_size-self.win_size+1):    #columns
                second_diagonal.append([])
                for k in range(self.win_size):                  #length of each win
                    second_diagonal[(i-self.win_size+1)*(self.board_size-self.win_size+1)+j].append((i-k,j+k))
        return rows + columns + first_diagonal + second_diagonal

    def is_valid_move(self, move):
        """Returns True if move is valid->no winner yet and square is empty"""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
    
    def process_move(self, move):
        """Makes move and checks if current move is win"""
        row, col = move.row, move.col
        self._current_moves[row][col] = move    #input assigned to [row][col] in current moves
        for combo in self._winning_combos:      #loop over winning combos
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results)==1) and (""not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """True if game has winner"""
        return self._has_winner
    
    def is_tied(self):
        """Checks if game is tied"""
        no_winner = not self._has_winner    #no winner yet
        #check if all cells have a string->a move
        played_moves = (move.label for row in self._current_moves for move in row)
        return no_winner and all(played_moves)
    
    def toggle_player(self):
        """Cicles between players"""
        self.current_player = next(self._players)
    
    def reset_game(self):
        """Starts a new game"""
        for row, row_content in enumerate(self._current_moves):     #resets all moves to empty
            for col,_ in enumerate(row_content):
                row_content[col]=Move(row, col)
        self._has_winner = False    #resets winner
        self.winner_combo = []      #resets winning move



class TicTacToeBoard(tk.Tk):                #class inherits from Tk
    def __init__(self, game):
        super().__init__()                  #initialize parent class
        self.title("Mega Tic-Tac-Toe")      #title bar
        self._cells = {}                     #dictionary for row and column of cells
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)       #frame object holds display, main window is parent
        display_frame.pack(fill=tk.X)               #fill's screen with game board
        self.display = tk.Label(master=display_frame, 
                                text="Ready?", 
                                font=font.Font(size=28, weight="bold"))
        self.display.pack()

    def _create_board_grid(self): 
        grid_frame = tk.Frame(master = self)    #create frame for board frame
        grid_frame.pack()                       #puts it on main window
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)        #cell weidght and height
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(master=grid_frame, text="", 
                                font = font.Font(size=24, weight="bold"),
                                fg="black", width=3, height=2,
                                highlightbackground="lightblue")
                self._cells[button] = (row,col)             #adds every new button to the dictionary
                button.bind("<ButtonPress-1>", self.play)    #play gets run when button is pressed
                button.grid(row=row, column=col,padx=5,pady=5,sticky="nsew")
    
    def play(self, event):
        """Handles player moves""" 
        clicked_btn = event.widget              #retrieves button that triggered event
        row, col = self._cells[clicked_btn]     #cell's coordinates
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):      #if move is valid
            self._update_button(clicked_btn)    #set button to player
            self._game.process_move(move)       #process move
            if self._game.is_tied():            #check if game is tied
                self._update_display(msg = "Tied!", color = "green")
            elif self._game.has_winner():       #check if game is won
                self._highlight_cells()         #highlight winning cells
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)    #update display to winner message
            else:
                self._game.toggle_player()      #no winner or tie->continue with next player
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
    
    def _update_button(self, clicked_btn):
        """Updates button to current player's"""
        clicked_btn.config(text = self._game.current_player.label)
        clicked_btn.config(fg = self._game.current_player.color)
    
    def _update_display(self, msg, color="black"):
        """Updates game display"""
        self.display["text"] = msg
        self.display["fg"] = color
    
    def _highlight_cells(self):
        """Highlighting cells for a win"""
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground = "red")

    def _create_menu(self):
        """Creates menu bar to exit and play again"""
        menu_bar = tk.Menu(master = self)       #instance of menu -> menu bar
        self.config(menu=menu_bar)              #menu bar is main menu
        file_menu = tk.Menu(master = menu_bar)  #creates instance of menu -> file menu
        file_menu.add_command(                  #new command in file menu
            label = "Play Again",               #play again is the name
            command = self.reset_board          #resets the board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command = quit)     #adds exit
        menu_bar.add_cascade(label="File", menu = file_menu)    #adds file
    
    def reset_board(self):
        """Resets the game board"""
        self._game.reset_game()         #calls upon reset_game method
        self._update_display(msg = "Ready?")    #reset board display
        for button in self._cells.keys():       #loops over each button to reset them
            button.config(highlightbackground = "lightblue")
            button.config(text = "")
            button.config(fg = "black")


#initializes game
def main():
    start = StartScreen()
    start.mainloop()
    game = TicTacToeGame(board_size=int(BOARD_SIZE),
                         win_size=int(WIN_SIZE))
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()
