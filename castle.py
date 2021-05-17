def can_castle_kingside(board, king_row, king_col):
    if king_col != 4:
        return False

    king = board[king_row][king_col]
    rook = board[king_row][king_col + 3]

    if not king or not rook or king.has_moved or rook.has_moved:
        return False

    # Check that king and rook are there and no pieces between them
    return board[king_row][king_col + 1] is None and board[king_row][king_col + 2] is None
    
def can_castle_queenside(board, king_row, king_col):
    if king_col != 4:
        return False

    king = board[king_row][king_col]
    rook = board[king_row][king_col - 4]

    if not king or not rook or king.has_moved or rook.has_moved:
        return False

    return board[king_row][king_col - 1] is None and board[king_row][king_col - 2] is None and board[king_row][king_col - 3] is None

def move_is_kingside_castle(board, move):
    start_coord, end_coord = move
    piece = board[start_coord[0]][start_coord[1]]

    return piece and piece.piece_type == "K" and start_coord[0] == end_coord[0] and (end_coord[1] - start_coord[1] == 2)

def move_is_queenside_castle(board, move):
    start_coord, end_coord = move
    piece = board[start_coord[0]][start_coord[1]]

    return piece and piece.piece_type == "K" and start_coord[0] == end_coord[0] and (start_coord[1] - end_coord[1] == 2)