from moves import is_king_checked

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

def print_board(board, current_turn):
    for i in range(8):
        for j in range(8):
            print_piece(board[i][j])
        print("\r")
    print("Current turn: " + current_turn)
    if is_king_checked(board, current_turn):
        print(current_turn + " is in Check!")
    print("\r")