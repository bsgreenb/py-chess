import copy
import castle
import check

# TODO: handle queen promotion
# TODO: add enpassant (QSTN: is this a pawn only capture?)

def get_pawn_attacks(board, row, col):
    pawn_attacks = []

    pawn = board[row][col]
    current_team = pawn.team

    row_delta = -1 if current_team == "white" else 1
    other_team = "black" if current_team == "white" else "white" 

    for col_delta in (-1, 1):
        attack_row = row + row_delta
        attack_col = col + col_delta
        
        # Attack row will always be in range of the board because it gets promoted at end.
        if attack_col not in range(7):
            continue 

        attacked_piece = board[attack_row][attack_col]
        if (attacked_piece and attacked_piece.team == other_team):
            pawn_attacks.append([attack_row, attack_col])

    return pawn_attacks

def get_pawn_moves(board, row, col):
    pawn_moves = []

    pawn = board[row][col]
    current_team = pawn.team

    row_delta = -1 if current_team == "white" else 1
    starting_row = 6 if current_team == "white" else 1

    # Can go forward 1 step if there's no piece there
    if board[row + row_delta][col] is None:
        pawn_moves.append([row + row_delta, col])

    # Can go forward 2 steps if on starting row and no pieces in the way    
    if (row == starting_row) and board[row + row_delta][col] is None and board[row + (row_delta * 2)][col] is None:
        pawn_moves.append([row + (row_delta * 2), col])
    
    pawn_moves.extend(get_pawn_attacks(board, row, col))

    return pawn_moves
    
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
    

def get_king_moves(board, row, col, allow_check = False):
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

    # Prevent infinite loop of checking kings for check
    if castle.can_castle_kingside(board, row, col, allow_check):
        moves.append([row, col + 2])

    if castle.can_castle_queenside(board, row, col, allow_check):
        moves.append([row, col - 2])
    
    return moves

def get_piece_attacks(board, row, col):
    piece = board[row][col]
    if piece.piece_type == "P":
        return get_pawn_attacks(board, row, col)
    else:
        return get_piece_legal_moves(board, row, col, True)

def get_piece_legal_moves(board, row, col, allow_check = False):
    piece = board[row][col]
    current_turn = piece.team

    if piece.piece_type == "P":
        piece_moves = get_pawn_moves(board, row, col)
    elif piece.piece_type == "N":
        piece_moves = get_knight_moves(board, row, col)
    elif piece.piece_type == "B":
        piece_moves = get_bishop_moves(board, row, col)
    elif piece.piece_type == "R":
        piece_moves = get_rook_moves(board, row, col)
    elif piece.piece_type == "Q":
        piece_moves = get_queen_moves(board, row, col) # this can be bishop and rook together
    elif piece.piece_type == "K":
        piece_moves = get_king_moves(board, row, col, allow_check)

    # Add back starting coordinate
    piece_moves = list(map(lambda move: [[row, col], move], piece_moves))

    if allow_check:
        return piece_moves
    else:
        return check.get_non_checked_moves(board, current_turn, piece_moves)

# Returns a hypothetical board when a move is made.  Apply_move uses this, as does get_legal_moves, for checking hypothetical board for check etc.
def make_move(board, move):
    board = copy.deepcopy(board)
    if (castle.move_is_kingside_castle(board, move)):
        king = board[move[0][0]][move[0][1]]
        rook = board[move[0][0]][move[0][1] + 3]

        board[move[0][0]][move[0][1]] = None
        board[move[0][0]][move[0][1] + 3] = None

        board[move[0][0]][move[0][1] + 1] = rook
        board[move[0][0]][move[0][1] + 2] = king

    elif (castle.move_is_queenside_castle(board, move)):
        king = board[move[0][0]][move[0][1]]
        rook = board[move[0][0]][move[0][1] - 4]

        board[move[0][0]][move[0][1]] = None
        board[move[0][0]][move[0][1] - 4] = None

        board[move[0][0]][move[0][1] - 1] = rook
        board[move[0][0]][move[0][1] - 2] = king
        
    else:
        # Normal move
        start_coord, end_coord = move
        
        board[end_coord[0]][end_coord[1]] = board[start_coord[0]][start_coord[1]]
        board[start_coord[0]][start_coord[1]] = None

    return board

