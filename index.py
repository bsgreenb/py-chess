from enum import Enum  

# Continya at https://levelup.gitconnected.com/chess-python-ca4532c7f5a4

class Team(Enum):
    B = 'black'
    W = 'white'

class PieceType(Enum):
    P = 'pawn'
    N = 'knight'
    B = 'bishop'
    R = 'rook'
    Q = 'queen'
    K = 'king'

class Piece:
    def __init__(self, team, piece_type):
        self.team = team
        self.piece_type = piece_type

black_pawn = Piece(Team.B, PieceType.P)
black_knight = Piece(Team.B, PieceType.N)
black_bishop = Piece(Team.B, PieceType.B)
black_rook = Piece(Team.B, PieceType.R)
black_queen = Piece(Team.B, PieceType.Q)
black_king = Piece(Team.B, PieceType.K)

white_pawn = Piece(Team.W, PieceType.P)
white_knight = Piece(Team.W, PieceType.N)
white_bishop = Piece(Team.W, PieceType.B)
white_rook = Piece(Team.W, PieceType.R)
white_queen = Piece(Team.W, PieceType.Q)
white_king = Piece(Team.W, PieceType.K)

board = [[None for i in range(8)] for i in range(8)]

def initialize_board(board):
    for i in range(8):
        board[1][i] = black_pawn
        board[6][i] = white_pawn

    return board

board = initialize_board(board)

print(board)