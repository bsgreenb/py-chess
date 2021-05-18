import moves
import display
import check

class IllegalMoveError(Exception):
    pass

class Piece:
    def __init__(self, team, piece_type):
        self.team = team
        self.piece_type = piece_type
        self.has_moved = None

class Game:
    def __init__(self, board = None):
        if board is None:
            self.setup_board()
        else:
            self.board = board
        
        self.current_turn = "white"
        self.move_history = []

    def setup_board(self):
        board = [[None for col in range(8)] for row in range(8)]

        black_pawn = Piece("black", "P")
        black_knight = Piece("black", "N")
        black_bishop = Piece("black", "B")
        black_rook = Piece("black", "R")
        black_queen = Piece("black", "Q")
        black_king = Piece("black", "K")

        white_pawn = Piece("white", "P")
        white_knight = Piece("white", "N")
        white_bishop = Piece("white", "B")
        white_rook = Piece("white", "R")
        white_queen = Piece("white", "Q")
        white_king = Piece("white", "K")

        for col in range(8):
            board[1][col] = black_pawn
            board[6][col] = white_pawn

            board[0] = [black_rook, black_knight, black_bishop, black_queen, black_king, black_bishop, black_knight, black_rook]
            board[7] = [white_rook, white_knight, white_bishop, white_queen, white_king, white_bishop, white_knight, white_rook]

        self.board = board
    
    def switch_turn(self):
        if self.current_turn == "white":
            self.current_turn = "black"
        else:
            self.current_turn = "white"

    def move_square_to_coordinates(self, square):
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

        row = 8 - int(square[1])

        return [row, col]

    def move_to_coordinates(self, move):
        return [self.move_square_to_coordinates(move[:2]), self.move_square_to_coordinates(move[2:4])]

    def apply_move(self, move):
        move = self.move_to_coordinates(move)
        legal_moves = self.get_legal_moves()
        
        if move not in legal_moves:
            raise IllegalMoveError

        moving_piece = self.board[move[0][0]][move[0][1]]

        if moving_piece.piece_type in ("K", "R"):
            moving_piece.has_moved = True

        self.board = moves.make_move(self.board, move)

        self.move_history.append(move)
        self.switch_turn()

    def get_legal_moves(self):
        legal_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.team == self.current_turn:
                    # Only look at the current player's pieces
                    
                    # Map in starting position of the piece
                    piece_moves = moves.get_piece_legal_moves(self.board, row, col)
                    legal_moves.extend(piece_moves)

        return legal_moves

    def play_game(self):
        while True:
            display.print_board(self.board, self.current_turn)
            legal_moves = self.get_legal_moves()

            if len(legal_moves) == 0:
                if check.is_king_checked(self.board, self.current_turn):
                    other_team = "white" if self.current_turn == "black" else "black"
                    print(other_team + " wins by checkmate")
                    return 1 if self.current_turn == "black" else -1
                else:
                    print("Game is a draw via stalemate")
                    return 0
            
            if check.is_king_checked(self.board, self.current_turn):
                print(self.current_turn + " is in Check!")

            next_move = input("What's your move? E.g. e4e5\n")
            try:
                self.apply_move(next_move)
            except IllegalMoveError:
                print("Illegal Move!")
if __name__ == '__main__':
    game = Game()
    game.play_game()

#TODO: implement Game class, which will have board and turn variables instead of these globals