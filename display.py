
# Later: https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode
def print_piece(piece):
    if piece is None:
        print(".", end =" ")
        return

    piece_type = piece.piece_type

    white_display = {
        "K": "♚",
        "Q": "♛",
        "R": "♜",
        "B": "♝",
        "N": "♞",
        "P": "♟︎"
    }

    black_display = {
        "K": "♔",
        "Q": "♕",
        "R": "♖",
        "B": "♗",
        "N": "♘",
        "P": "♙"
    }
    

    if (piece.team == "white"):
        print(white_display[piece_type], end = " ")
    else:
        print(black_display[piece_type], end = " ")

def print_board(board, current_turn):
    print("\r")
    for i in range(8):
        for j in range(8):
            print_piece(board[i][j])
        print("\r")
    print("Current turn: " + current_turn)
    print("\r")