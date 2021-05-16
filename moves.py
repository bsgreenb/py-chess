import copy

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

def move_is_kingside_castle(board, move):
    start_coord, end_coord = move
    piece = board[start_coord[0]][start_coord[1]]

    return piece and piece.piece_type == "K" and start_coord[0] == end_coord[0] and (end_coord[1] - start_coord[1] == 2)

def move_is_queenside_castle(board, move):
    start_coord, end_coord = move
    piece = board[start_coord[0]][start_coord[1]]

    return piece and piece.piece_type == "K" and start_coord[0] == end_coord[0] and (start_coord[1] - end_coord[1] == 2)


# Gets the square of the current turn's king
def get_king_square(board, current_turn):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.piece_type == "K" and piece.team == current_turn:
                return [row, col]

# TODO: address the issue with each side being in check.
def is_square_attacked(board, square, current_turn):
    # Loop through each of the opponents pieces and return True if we find one attacking the square
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.team != current_turn:
                piece_attacks = get_piece_attacks(board, row, col)
                for piece_attack in piece_attacks:
                    if square == piece_attack[1]:
                        return True

    return False
    


def is_king_checked(board, current_turn):
    king_square = get_king_square(board, current_turn)

    return is_square_attacked(board, king_square, current_turn)

# Filters moves for whether there's a check
def get_non_checked_moves(board, current_turn, piece_moves):
    non_checked_moves = []

    for piece_move in piece_moves:
        potential_board = make_move(board, piece_move)

        king_square = get_king_square(potential_board, current_turn)

        if not is_square_attacked(potential_board, king_square, current_turn):
            non_checked_moves.append(piece_move)
    
    return non_checked_moves

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
        piece_moves = get_king_moves(board, row, col)

    # Add back starting coordinate
    piece_moves = list(map(lambda move: [[row, col], move], piece_moves))

    if allow_check:
        return piece_moves
    else:
        return get_non_checked_moves(board, current_turn, piece_moves)

# Returns a hypothetical board when a move is made.  Apply_move uses this, as does get_legal_moves, for checking hypothetical board for check etc.
def make_move(board, move):
    board = copy.deepcopy(board)
    if (move_is_kingside_castle(board, move)):
        king = board[move[0][0]][move[0][1]]
        rook = board[move[0][0]][move[0][1] + 3]

        board[move[0][0]][move[0][1]] = None
        board[move[0][0]][move[0][1] + 3] = None

        board[move[0][0]][move[0][1] + 1] = rook
        board[move[0][0]][move[0][1] + 2] = king

    elif (move_is_queenside_castle(board, move)):
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

