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

# TODO: handle queen promotion
# TODO: add enpassant (QSTN: is this a pawn only capture?)
def get_pawn_moves_white(row, col):
    pawn_moves = []
    # Can go forward 1 step if there's no piece there
    if board[row - 1][col] is None:
        pawn_moves.append([row - 1, col])

    # Can go forward 2 steps if on starting row and no pieces in the way    
    if (row == 6) and board[row - 1][col] is None and board[row - 2][col] is None:
        pawn_moves.append([row - 2, col])
    
    # Can take black pieces diagonal forward-left
    if col != 0 and board[row - 1][col - 1] and board[row - 1][col - 1].team == "black":
        pawn_moves.append([row - 1, col - 1])

    # Can take black pieces diagonal forward-right
    if col != 7 and board[row - 1][col + 1] and board[row - 1][col + 1].team == "black":
        pawn_moves.append([row - 1, col + 1])

    return pawn_moves

def get_pawn_moves_black(row, col):
    pawn_moves = []
    # Can go forward 1 step if there's no piece there
    if board[row + 1][col] is None:
        pawn_moves.append([row + 1, col])

    # Can go forward 2 steps if on starting row and no pieces in the way    
    if (row == 1) and board[row + 1][col] is None and board[row + 2][col] is None:
        pawn_moves.append([row + 2, col])
    
    # Can take black pieces diagonal forward-right
    if col != 0 and board[row + 1][col - 1] and board[row + 1][col - 1].team == "white":
        pawn_moves.append([row + 1, col - 1])

    # Can take black pieces diagonal forward-left
    if col != 7 and board[row + 1][col + 1] and board[row + 1][col + 1].team == "white":
        pawn_moves.append([row + 1, col + 1])

    return pawn_moves

def get_pawn_moves(row, col):
    if current_turn == "white":
        return get_pawn_moves_white(row, col)
    else:
        return get_pawn_moves_black(row, col)
    
def is_valid_coordinate(row, col):
    return row in range(8) and col in range(8)

def get_knight_moves(row, col):
    moves = []

    potential_moves = [
        [row - 2, col - 1],
        [row - 2, col + 1],
        [row - 1, col + 2],
        [row - 1, col - 2],
        [row + 1, col + 2],
        [row + 1, col - 2],
        [row + 2, col + 1],
        [row + 2, col - 1]
    ]

    for potential_move in potential_moves:
        if is_valid_coordinate(potential_move[0], potential_move[1]):
            piece = board[potential_move[0]][potential_move[1]]
            if piece is None or piece.team != current_turn:
                moves.append(potential_move)
    
    return moves

# TODO: write dis
def get_bishop_moves(row, col):
    return []

def get_rook_moves(row, col):
    moves = []

    for horizontal_delta in (1, -1):
        move_col = col + horizontal_delta
        while True:
            if not is_valid_coordinate(row, move_col):
                break
            else:
                piece = board[row][move_col]
                if piece is None:
                    moves.append([row, move_col])
                    move_col = move_col + horizontal_delta
                elif piece.team != current_turn:
                    moves.append([row, move_col])
                    break
                else:
                    break
    
    for vertical_delta in (1, -1):
        move_row = row + vertical_delta
        while True:
            if not is_valid_coordinate(move_row, col):
                break
            else:
                piece = board[move_row][col]
                if piece is None:
                    moves.append([move_row, col])
                    move_row = move_row + vertical_delta
                elif piece.team != current_turn:
                    moves.append([move_row, col])
                    break
                else:
                    break

    return moves

def get_queen_moves(row, col):
    moves = get_bishop_moves(row, col)
    moves.extend(get_rook_moves(row, col))
    
    return moves

# TODO: write dis
def get_king_moves(row, col):
    return []

def get_piece_legal_moves(row, col):
    #TODO: add the starting coordinate so we can simplify the helpers
    piece = board[row][col]
    if piece.piece_type == "P":
        return get_pawn_moves(row, col)
    elif piece.piece_type == "N":
        return get_knight_moves(row, col)
    elif piece.piece_type == "B":
        return get_bishop_moves(row, col)
    elif piece.piece_type == "R":
        return get_rook_moves(row, col)
    elif piece.piece_type == "Q":
        return get_queen_moves(row, col) # this can be bishop and rook together
    elif piece.piece_type == "K":
        return get_king_moves(row, col)

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


