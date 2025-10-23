import unittest
from unittest.mock import patch, MagicMock
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

    def test_current_other_y_end_turn(self):
        self.assertIs(self.game.current_player(), self.pw)
        self.assertIs(self.game.other_player(), self.pb)
        self.game.end_turn()
        self.assertIs(self.game.current_player(), self.pb)
        self.assertIs(self.game.other_player(), self.pw)

    def test_roll_no_doble_y_doble(self):
        self.dice.roll.return_value = (3, 5)
        r = self.game.roll()
        self.assertEqual(r, (3, 5))
        self.assertCountEqual(self.game.get_available_moves(), [3, 5])
        self.dice.roll.return_value = (4, 4)
        r2 = self.game.roll()
        self.assertEqual(r2, (4, 4))
        self.assertEqual(self.game.get_available_moves(), [4, 4, 4, 4])

    def test_get_available_moves_es_copia_y_consume(self):
        self.dice.roll.return_value = (2, 5)
        self.game.roll()
        m = self.game.get_available_moves()
        m.append(99)
        self.assertEqual(self.game.get_available_moves(), [2, 5])
        self.assertTrue(self.game.consume_move_value(2))
        self.assertEqual(self.game.get_available_moves(), [5])
        self.assertFalse(self.game.consume_move_value(6))

    def test_helpers(self):
        self.assertEqual(self.game.direction("white"), 1)
        self.assertEqual(self.game.direction("black"), -1)
        self.assertEqual(self.game.entry_point_for_die("white", 3), 2)
        self.assertEqual(self.game.entry_point_for_die("black", 3), 21)
        self.assertEqual(self.game.distance("white", 5, 9), 4)
        self.assertEqual(self.game.distance("black", 9, 5), 4)


