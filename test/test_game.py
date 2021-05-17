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

if __name__ == '__main__':
    unittest.main()