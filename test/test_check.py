import unittest
from game import *

class TestCheck(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.board = [[None for col in range(8)] for row in range(8)]

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

        self.assertRaises(IllegalMoveError, game.apply_move, "d2d3")

    def test_canMoveKingInFrontOfPawn(self):
        white_king = Piece("white", "K")
        black_pawn = Piece("black", "P")

        self.board[7][4] = white_king
        self.board[6][3] = black_pawn

        game = Game(self.board)

        game.apply_move("e1d1")

        self.assertEqual(game.board[7][3].piece_type, "K")

    def test_cantMoveKingNextToKing(self):
        white_king = Piece("white", "K")
        black_king = Piece("black", "K")

        self.board[7][4] = white_king
        self.board[7][6] = black_king

        game = Game(self.board)

        self.assertRaises(IllegalMoveError, game.apply_move, "e1f1")

if __name__ == '__main__':
    unittest.main()
    