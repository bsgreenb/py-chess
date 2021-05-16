# TODO: handle queen promotion
# TODO: add enpassant (QSTN: is this a pawn only capture?)
def get_pawn_moves_white(board, row, col):
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

def get_pawn_moves_black(board, row, col):
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

def get_pawn_moves(board, row, col):
    piece = board[row][col]

    if piece.team == "white":
        return get_pawn_moves_white(board, row, col)
    else:
        return get_pawn_moves_black(board, row, col)
    
def is_valid_coordinate(row, col):
    return row in range(8) and col in range(8)

def get_knight_moves(board, row, col):
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

    piece = board[row][col]

    for potential_move in potential_moves:
        if is_valid_coordinate(potential_move[0], potential_move[1]):
            other_piece = board[potential_move[0]][potential_move[1]]
            if other_piece is None or other_piece.team != piece.team:
                moves.append(potential_move)
    
    return moves

def get_bishop_moves(board, row, col):
    moves = []

    piece = board[row][col]

    for delta in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        move_row = row + delta[0]
        move_col = col + delta[1]

        while True:
            if not is_valid_coordinate(move_row, move_col):
                break
            else:
                other_piece = board[move_row][move_col]
                if other_piece is None:
                    moves.append([move_row, move_col])
                    move_row = move_row + delta[0]
                    move_col = move_col + delta[1]
                elif other_piece.team != piece.team:
                    moves.append([move_row, move_col])
                    break
                else:
                    break
        
    return moves               

def get_rook_moves(board, row, col):
    moves = []

    piece = board[row][col]

    for horizontal_delta in (1, -1):
        move_col = col + horizontal_delta
        while True:
            if not is_valid_coordinate(row, move_col):
                break
            else:
                other_piece = board[row][move_col]
                if other_piece is None:
                    moves.append([row, move_col])
                    move_col = move_col + horizontal_delta
                elif other_piece.team != piece.team:
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
                other_piece = board[move_row][col]
                if other_piece is None:
                    moves.append([move_row, col])
                    move_row = move_row + vertical_delta
                elif other_piece.team != piece.team:
                    moves.append([move_row, col])
                    break
                else:
                    break

    return moves

def get_queen_moves(board, row, col):
    moves = get_bishop_moves(board, row, col)
    moves.extend(get_rook_moves(board, row, col))
    
    return moves

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
    

# TODO: here is where we wanna add castling
def get_king_moves(board, row, col):
    moves = []
    piece = board[row][col]

    for delta in ((-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)):
        move_row = row + delta[0]
        move_col = col + delta[1]

        if is_valid_coordinate(move_row, move_col):
            other_piece = board[move_row][move_col]
            if other_piece is None or other_piece.team != piece.team:
                moves.append([move_row, move_col])

    if can_castle_kingside(board, row, col):
        moves.append([row, col + 2])

    if can_castle_queenside(board, row, col):
        moves.append([row, col - 2])
    
    return moves

