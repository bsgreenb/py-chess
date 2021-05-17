import moves

# Gets the square of the current turn's king
def get_king_square(board, current_turn):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.piece_type == "K" and piece.team == current_turn:
                return [row, col]

def is_square_attacked(board, square, current_turn):
    # Loop through each of the opponents pieces and return True if we find one attacking the square
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.team != current_turn:
                piece_attacks = moves.get_piece_attacks(board, row, col)
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
        potential_board = moves.make_move(board, piece_move)

        king_square = get_king_square(potential_board, current_turn)

        if not is_square_attacked(potential_board, king_square, current_turn):
            non_checked_moves.append(piece_move)
    
    return non_checked_moves