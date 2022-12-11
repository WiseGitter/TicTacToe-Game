import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

"""Defining the size of grids and the color and labels of the characters inside the cells"""
BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="red"),
    Player(label="O", color="green"),
)

"""Creating a class to represent the game board and initialising all the attributes such 
as the players, board size, winning combinations etc"""
class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()
    """We use a list comprehension to provide an initial list for the current moves. An empty move stores the 
coordinated of its containing cells and the empty string as the initial player's label"""
    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()  #We call the Winning_combos methodand assigns it's returns to
                                                            # winning combos


    """This method gives us the 8 possibilities of a player to win the game, That is horizontally, 
    vertically and diagonally. The main input for this method is the current_moves attribute
    """
    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    """This method is simply for returning to the other player is one player made it's move, using the next command."""
    def toggle_player(self):
        self.current_player = next(self._players)

    """Checking if the move is valid, There are only 2 conditions that make a move valid, If the game hasn't
    already been finished or if the given cell has not been played already."""
    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    """The process move method is used to check if the last winner has won the game or not.
    To find out if there is a winner we check if a particular player's label is present in all the cells in a 
     given winning combination"""
    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)   #Retriving all the winning combinations
                                                                         #and converts it into a set object
            is_win = (len(results) == 1) and ("" not in results)    #Defines a boolean expression to check if the current
                                                   # move determined a win or not amnd stores the result to is_win
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    """Return True if the game has a winner, and False if no winner."""
    def has_winner(self):
          return self._has_winner

    """Checking for a tie. The game is a tie in 2 cases. Either all the moves are played, or there is no winner."""
    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    """Reset the game state to play again."""
    def reset_game(self):
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

"""Creating a TicTacToeBoard class to represent the playing board. Using the Tk class which allows to create the 
main window of the TKinter app."""
class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Let's Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    """Creating a board display method with the master argument set to self, saying that the game's main window will be 
    the frame's parent. This is to ensure the game's state and result, and the pack command it used to resize the 
    game frame according to the user and resize the shape of the cells accordingly"""
    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Let's Go?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()


    """Creating a board grid method that ensure a lot of work fir the cells or the grid of the game in which the labels
    would be entered by the users. Creating a loop that iterates from 0 to 2 to represent the number of grids
    in the game, which usually is 3x3. However we can change it if we want"""
    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                """Creating a button object for all the cells with several attributes"""
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                """The below statement add every statement to the ._cells dictionary. Button = keys and (row,col) =  values"""
                self._cells[button] = (row, col)
                """The .bind command is activated at the click event of any button. This way if any of the player
                makes a move then the methd will run to process and update the game state"""
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")     #Add every button to the main window
                                                                                #using the .grid command

    """Handling a players move. It defines a Play method with the main arguments as self and the Ktinker object"""
    def play(self, event):
        """This retrieves the widget(buttons) that triggered the current event."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        """The below statements update the game frame by calling the methods .update_button() and .process.move()"""
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
                """The code below Checks if the game has a winner or not, if True, then it highlights the 
                winning cells. And then the following lines acknoledge the player who won the game."""
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
                """Below code : If the game isn't tied and no player won then the below code get's executed"""
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()