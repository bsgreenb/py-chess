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

board = [[None for i in range(8)] for i in range(8)]

def initialize_board(board):
    for i in range(8):
        board[1][i] = black_pawn
        board[6][i] = white_pawn

    board[0] = [black_rook, black_knight, black_bishop, black_queen, black_king, black_bishop, black_knight, black_rook]
    board[7] = [white_rook, white_knight, white_bishop, white_queen, white_king, white_bishop, white_knight, white_rook]

    return board

board = initialize_board(board)

    
def print_piece(piece):
    if piece is None:
        print(".", end =" ")
        return

    piece_type = piece.piece_type
    if (piece.team == "white"):
        print(piece_type, end =" ")
    else:
        print(piece_type.lower(), end =" ")

def print_board(board):
    for i in range(8):
        for j in range(8):
            print_piece(board[i][j])
        print("\r")

print_board(board)