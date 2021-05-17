import unittest
from game import *

# CONTINYA: apply fix from https://stackoverflow.com/questions/67542106/relative-import-error-using-python-unittest

class TestGame(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.board = [[None for col in range(8)] for row in range(8)]


    def test_pawn(self):
        white_pawn = Piece("white", "P")

        self.board[6][4] = white_pawn

        game = Game(self.board)
        game.apply_move("e2e3")

        self.assertEqual(game.board[5][4].piece_type, "P")
        self.assertIsNone(game.board[6][4])

    def test_castleKingside(self):
        white_king = Piece("white", "K")
        white_rook = Piece("white", "R")

        self.board[7][4] = white_king
        self.board[7][7] = white_rook

        game = Game(self.board)

        game.apply_move("e1g1")

        self.assertEqual(game.board[7][5].piece_type, "R")
        self.assertEqual(game.board[7][6].piece_type, "K")

    def test_castleKingside_black(self):
        black_king = Piece("black", "K")
        black_rook = Piece("black", "R")

        self.board[0][4] = black_king
        self.board[0][7] = black_rook

        game = Game(self.board)
        game.current_turn = "black"

        game.apply_move("e8g8")

        self.assertEqual(game.board[0][5].piece_type, "R")
        self.assertEqual(game.board[0][6].piece_type, "K")
    
    def test_castleQueenside(self):
        white_king = Piece("white", "K")
        white_rook = Piece("white", "R")

        self.board[7][0] = white_rook
        self.board[7][4] = white_king

        game = Game(self.board)

        game.apply_move("e1c1")

        self.assertEqual(game.board[7][2].piece_type, "K")
        self.assertEqual(game.board[7][3].piece_type, "R")
        
    def test_castleKingsideKingMoved(self):
        white_king = Piece("white", "K")
        white_rook = Piece("white", "R")

        self.board[7][4] = white_king
        self.board[7][7] = white_rook

        game = Game(self.board)
        game.apply_move("e1f1")
        game.current_turn = "white"
        game.apply_move("f1e1")
        game.current_turn = "white"

        self.assertRaises(IllegalMoveError, game.apply_move,"e1g1")
    
    def test_cantMoveKingIntoCheck(self):
        white_king = Piece("white", "K")
        black_bishop = Piece("black", "B")

        self.board[7][4] = white_king
        self.board[6][4] = black_bishop
        
        game = Game(self.board)
        
        self.assertRaises(IllegalMoveError, game.apply_move, "e1f1")

    def test_cantDiscoverSelfCheck(self):
        white_king = Piece("white", "K")
        white_pawn = Piece("white", "P")
        black_bishop = Piece("black", "B")

        self.board[7][4] = white_king
        self.board[6][3] = white_pawn
        self.board[5][2] = black_bishop
        
        game = Game(self.board)

        print_board(game.board, "white")
        
        self.assertRaises(IllegalMoveError, game.apply_move, "d2d3")

    def test_canMoveKingInFrontOfPawn(self):
        white_king = Piece("white", "K")
        black_pawn = Piece("black", "P")

        self.board[7][4] = white_king
        self.board[6][3] = black_pawn

        game = Game(self.board)

        game.apply_move("e1d1")

        self.assertEqual(game.board[7][3].piece_type, "K")

    
        

if __name__ == '__main__':
    unittest.main()