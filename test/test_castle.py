import unittest
from game import *
from castle import *

class TestGame(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.board = [[None for col in range(8)] for row in range(8)]
    
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