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
        game.make_move("e2e3")

        self.assertEqual(game.board[5][4], white_pawn)
        self.assertIsNone(game.board[6][4])

    def test_castleKingside(self):
        white_king = Piece("white", "K")
        white_rook = Piece("white", "R")

        self.board[7][4] = white_king
        self.board[7][7] = white_rook

        game = Game(self.board)

        game.make_move("e1g1")

        self.assertEqual(game.board[7][5], white_rook)
        self.assertEqual(game.board[7][6], white_king)

    def test_castleKingside_black(self):
        black_king = Piece("black", "K")
        black_rook = Piece("black", "R")

        self.board[0][4] = black_king
        self.board[0][7] = black_rook

        game = Game(self.board)
        game.current_turn = "black"

        game.make_move("e8g8")

        self.assertEqual(game.board[0][5], black_rook)
        self.assertEqual(game.board[0][6], black_king)
    
    def test_castleQueenside(self):
        white_king = Piece("white", "K")
        white_rook = Piece("white", "R")

        self.board[7][0] = white_rook
        self.board[7][4] = white_king

        game = Game(self.board)

        game.make_move("e1c1")

        self.assertEqual(game.board[7][2], white_king)
        self.assertEqual(game.board[7][3], white_rook)
        
    def test_castleKingsideKingMoved(self):
        white_king = Piece("white", "K")
        white_rook = Piece("white", "R")

        self.board[7][4] = white_king
        self.board[7][7] = white_rook

        game = Game(self.board)
        game.make_move("e1f1")
        game.current_turn = "white"
        game.make_move("f1e1")
        game.current_turn = "white"

        self.assertRaises(IllegalMoveError, game.make_move,"e1g1")

if __name__ == '__main__':
    unittest.main()