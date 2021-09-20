""" A simple tictactoe program. The game is read after the board is read from a file. The file either already exists, the game
is already in play, or a blank board is displayed to the user. """
import json
from os import read

# The characters used in the Tic-Tac-Too board
X = 'X'
O = 'O'
Blank = ' '

# A blank Tic-Tac-Toe board
blank_board = {  
            "board": [
                Blank, Blank, Blank,
                Blank, Blank, Blank,
                Blank, Blank, Blank ]
        }

def read_board(filename):
    # Read the previously existing board from the file if it exists.
    try:
        with open(filename, "r") as file:
            board_text = file.read()
            board_json = json.loads(board_text)
            return board_json["board"]
    # Else display a blank board.
    except:
        return blank_board["board"]

def save_board(filename, board):
    # Save the current game to a file.
    with open(filename, "w") as file:
        board_json = {}
        board_json["board"] = board
        board_text = json.dumps(board_json)
        file.write(board_text)

def display_board(board):
    #Display a Tic-Tac-Toe board on the screen in a user-friendly way.
    print(" " + board[0] + " |" + " " +  board[1] + " |" + " " + board[2])
    print("---+---+---")
    print(" " + board[3] + " |" + " " +  board[4] + " |" + " " +  board[5])
    print("---+---+---")
    print(" " + board[6] + " |" + " " +  board[7] + " |" + " " +  board[8])
        

def is_x_turn(board):
    # Determine whose turn it is
    x_count = 0
    o_count = 0

    # Loop through the board and count number of x's and o's
    for i in board:
        if i == X:
            x_count += 1
        elif i == O:
            o_count += 1
        return x_count == o_count
    return True

def game_done(board, message=False):
    '''Determine if the game is finished'''
    # Game is finished if all the squares are filled
    tie = True
    for square in board:
        if square == Blank:
            tie = False
    if tie:
        if message:
            print("The game is a tie!")
        return True

    # Game is finished if someone has completed a row
    for row in range(3):
        if board[row * 3] != Blank and board[row * 3] == board[row * 3 + 1] == board[row * 3 + 2]:
            if message:
                print("The game was won by", board[row * 3])
            return True
    # Game is finished if someone has completed a column
    for col in range(3):
        if board[col] != Blank and board[col] == board[3 + col] == board[6 + col]:
            if message:
                print("The game was won by", board[col])
            return True
    # Game is finished if someone has a diagonal
    if board[4] != Blank and (board[0] == board[4] == board[8] or
                              board[2] == board[4] == board[6]):
        if message:
            print("The game was won by", board[4])
        return True
    return False

def play_game(board):
    # Play the game of Tic-Tac-Toe
    x_turn = is_x_turn(board)
    user_input = input("X>" if x_turn else "O>")
    # Verify that user_input is an integer else set it to -1
    square = int(user_input) - 1 if user_input.isdigit() else -1

    # Accept user input
    if 0 <= square <= 8:
        if board[square] == Blank:
            board[int(user_input)-1] = X if x_turn else O
        else:
            print("That square is taken. Try again")
        # Return True for the game loop to ask the user to play again.
        return True
    return False

# Read the board from a file if it exists
board = read_board("board.json")

# The file read code, game loop code, and file close code goes here
print("Enter 'q' to suspend your game. Otherwise, enter a number from 1 to 9")
print("where the following numbers correspond to the locations on the grid:")
print(" 1 | 2 | 3 ")
print("---+---+---")
print(" 4 | 5 | 6 ")
print("---+---+---")
print(" 7 | 8 | 9 \n")
print("The current board is:")
display_board(board)

# Run the game loop
while play_game(board) and not game_done(board, message=True):
    display_board(board)

# Save the current board
save_board("board.json", blank_board["board"] if game_done(board) else board)
