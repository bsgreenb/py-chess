from moves import *
from enum import Enum  

# Continya at https://levelup.gitconnected.com/chess-python-ca4532c7f5a4

teams = ("white", "black")

piece_types = {
    "pawn": "P",
    "knight": "N",
    "bishop": "B",
    "rook": "R",
    "queen": "Q",
    "king": "K"
}

class Piece:
    def __init__(self, team, piece_type):
        self.team = team
        self.piece_type = piece_type

black_pawn = Piece("black", piece_types["pawn"])
black_knight = Piece("black", piece_types["knight"])
black_bishop = Piece("black", piece_types["bishop"])
black_rook = Piece("black", piece_types["rook"])
black_queen = Piece("black", piece_types["queen"])
black_king = Piece("black", piece_types["king"])

white_pawn = Piece("white", piece_types["pawn"])
white_knight = Piece("white", piece_types["knight"])
white_bishop = Piece("white", piece_types["bishop"])
white_rook = Piece("white", piece_types["rook"])
white_queen = Piece("white", piece_types["queen"])
white_king = Piece("white", piece_types["king"])

board = [[None for col in range(8)] for row in range(8)]
move_history = []

def initialize_board():

    for col in range(8):
        board[1][col] = black_pawn
        board[6][col] = white_pawn

    board[0] = [black_rook, black_knight, black_bishop, black_queen, black_king, black_bishop, black_knight, black_rook]
    board[7] = [white_rook, white_knight, white_bishop, white_queen, white_king, white_bishop, white_knight, white_rook]

    return board

board = initialize_board()

    
# Later: https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode
def print_piece(piece):
    if piece is None:
        print(".", end =" ")
        return

    piece_type = piece.piece_type
    if (piece.team == "white"):
        print(piece_type, end =" ")
    else:
        print(piece_type.lower(), end =" ")

def print_board():
    for i in range(8):
        for j in range(8):
            print_piece(board[i][j])
        print("\r")


def move_square_to_coordinates(square):
    col = square[0].lower()

    if (col == "a"):
        col = 0
    elif (col == "b"):
        col = 1
    elif (col == "c"):
        col = 2
    elif (col == "d"):
        col = 3
    elif (col == "e"):
        col = 4
    elif (col == "f"):
        col = 5
    elif (col == "g"):
        col = 6
    elif (col == "h"):
        col = 7
    else:
        raise('Invalid column: ' + col)

    row = int(square[1])

    return [row, col]

def move_to_coordinates(move):
    return move_square_to_coordinates(move[:2]), move_square_to_coordinates(move[2:4])

current_turn = "white"

def get_piece_legal_moves(row, col):
    #TODO: add the starting coordinate so we can simplify the helpers
    piece = board[row][col]
    if piece.piece_type == "P":
        return get_pawn_moves(board, row, col)
    elif piece.piece_type == "N":
        return get_knight_moves(board, row, col)
    elif piece.piece_type == "B":
        return get_bishop_moves(board, row, col)
    elif piece.piece_type == "R":
        return get_rook_moves(board, row, col)
    elif piece.piece_type == "Q":
        return get_queen_moves(board, row, col) # this can be bishop and rook together
    elif piece.piece_type == "K":
        return get_king_moves(board, row, col)

# TODO: incorporate checks
def get_legal_moves():
    legal_moves = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.team == current_turn:
                # Only look at the current player's pieces
                
                # Map in starting position of the piece
                piece_moves = list(map(lambda move: [[row, col], move], get_piece_legal_moves(row, col)))
                legal_moves.extend(piece_moves)

    return legal_moves

def make_move(move):
    print(move_to_coordinates(first_move))

print_board()

print(get_legal_moves())

#first_move = input("What's your move? E.g. e4e5\n")

# TODO: get familiar with python debugger


