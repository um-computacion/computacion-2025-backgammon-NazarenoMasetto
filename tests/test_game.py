import unittest
from unittest.mock import MagicMock, patch

from core.game import BackgammonGame

class FakePlayer:
    def __init__(self, nombre, color):
        self._nombre = nombre
        self._color = color
        self._off = 0
    def get_color(self):
        return self._color
    def add_off(self, n):
        self._off += n
    def get_off_count(self):
        return self._off
    def get_nombre(self):
        return self._nombre

class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        self.pw = FakePlayer("W", "white")
        self.pb = FakePlayer("B", "black")
        self.p_board = patch("core.game.Board")
        self.p_dice = patch("core.game.Dice")
        self.MockBoard = self.p_board.start()
        self.MockDice = self.p_dice.start()
        self.addCleanup(self.p_board.stop)
        self.addCleanup(self.p_dice.stop)
        self.board = MagicMock()
        self.dice = MagicMock()
        self.MockBoard.return_value = self.board
        self.MockDice.return_value = self.dice
        self.game = BackgammonGame(self.pw, self.pb)

    def test_start_llama_setup(self):
        self.game.start()
        self.board.setup_start_position.assert_called_once()

    def test_current_y_other_player(self):
        self.assertIs(self.game.current_player(), self.pw)
        self.assertIs(self.game.other_player(), self.pb)
        self.game.end_turn()
        self.assertIs(self.game.current_player(), self.pb)
        self.assertIs(self.game.other_player(), self.pw)