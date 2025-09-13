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

    def test_roll_no_doble(self):
        self.dice.roll.return_value = (3, 5)
        r = self.game.roll()
        self.assertEqual(r, (3, 5))
        self.assertEqual(sorted(self.game.get_available_moves()), [3, 5])

    def test_roll_doble(self):
        self.dice.roll.return_value = (4, 4)
        r = self.game.roll()
        self.assertEqual(r, (4, 4))
        self.assertEqual(self.game.get_available_moves(), [4, 4, 4, 4])

    def test_consume_move_value(self):
        self.dice.roll.return_value = (2, 5)
        self.game.roll()
        ok = self.game.consume_move_value(2)
        self.assertTrue(ok)
        self.assertEqual(self.game.get_available_moves(), [5])
        self.assertFalse(self.game.consume_move_value(6))

    def test_end_turn_resetea(self):
        self.dice.roll.return_value = (1, 2)
        self.game.roll()
        self.game.end_turn()
        self.assertEqual(self.game.get_available_moves(), [])
        self.assertIs(self.game.current_player(), self.pb)

    def test_direction_entry_distance(self):
        self.assertEqual(self.game.direction("white"), 1)
        self.assertEqual(self.game.direction("black"), -1)
        self.assertEqual(self.game.entry_point_for_die("white", 3), 2)
        self.assertEqual(self.game.entry_point_for_die("black", 3), 23 - 2)
        self.assertEqual(self.game.distance("white", 5, 9), 4)
        self.assertEqual(self.game.distance("black", 9, 5), 4)

    def test_can_bear_off_white_exact_y_overflow_true_false(self):
        self.board.count_color_on_point.return_value = 0
        self.assertTrue(self.game.can_bear_off_with("white", 23, 1))
        self.assertTrue(self.game.can_bear_off_with("white", 22, 3))
        def count_white(i, color):
            return 1 if (color == "white" and i == 20) else 0
        self.board.count_color_on_point.side_effect = count_white
        self.assertFalse(self.game.can_bear_off_with("white", 22, 5))

    def test_can_bear_off_black_exact_y_overflow_true_false(self):
        self.board.count_color_on_point.return_value = 0
        self.assertTrue(self.game.can_bear_off_with("black", 0, 1))
        self.assertTrue(self.game.can_bear_off_with("black", 1, 3))
        def count_black(i, color):
            return 1 if (color == "black" and i == 4) else 0
        self.board.count_color_on_point.side_effect = count_black
        self.assertFalse(self.game.can_bear_off_with("black", 1, 5))

    def test_apply_move_falla_si_hay_bar_y_src_no_es_menos1(self):
        self.board.get_bar_count.return_value = 1
        self.dice.roll.return_value = (3, 4)
        self.game.roll()
        self.assertFalse(self.game.apply_move(5, 8))

    def test_apply_move_falla_sin_available(self):
        self.board.get_bar_count.return_value = 0
        self.assertFalse(self.game.apply_move(5, 8))