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

    def test_can_bear_off_white_exact_overflow_true_false(self):
        self.board.count_color_on_point.return_value = 0
        self.assertTrue(self.game.can_bear_off_with("white", 23, 1))
        self.assertTrue(self.game.can_bear_off_with("white", 22, 3))
        def cnt(i, col):
            return 1 if (col == "white" and i == 20) else 0
        self.board.count_color_on_point.side_effect = cnt
        self.assertFalse(self.game.can_bear_off_with("white", 22, 5))

    def test_can_bear_off_black_exact_overflow_true_false(self):
        self.board.count_color_on_point.return_value = 0
        self.assertTrue(self.game.can_bear_off_with("black", 0, 1))
        self.assertTrue(self.game.can_bear_off_with("black", 1, 3))
        def cnt(i, col):
            return 1 if (col == "black" and i == 4) else 0
        self.board.count_color_on_point.side_effect = cnt
        self.assertFalse(self.game.can_bear_off_with("black", 1, 5))

    def test_apply_move_falla_por_bar_con_fichas_y_sin_moves(self):
        self.board.get_bar_count.return_value = 1
        self.assertFalse(self.game.apply_move(5, 8))
        self.board.get_bar_count.return_value = 0
        self.assertFalse(self.game.apply_move(5, 8))

    def test_apply_move_desde_bar_ok_y_mismatch(self):
        self.board.get_bar_count.return_value = 1
        self.dice.roll.return_value = (2, 5)
        self.game.roll()
        self.board.move_from_bar.return_value = True
        dest_ok = self.game.entry_point_for_die("white", 2)
        self.assertTrue(self.game.apply_move(-1, dest_ok))
        self.assertFalse(self.game.apply_move(-1, 99))

    def test_apply_move_desde_bar_falla_en_board(self):
        self.board.get_bar_count.return_value = 1
        self.dice.roll.return_value = (3, 6)
        self.game.roll()
        self.board.move_from_bar.return_value = False
        dest_ok = self.game.entry_point_for_die("white", 3)
        self.assertFalse(self.game.apply_move(-1, dest_ok))

    def test_apply_move_bear_off_rechazado_por_all_in_home(self):
        self.board.get_bar_count.return_value = 0
        self.dice.roll.return_value = (2, 3)
        self.game.roll()
        self.board.all_in_home.return_value = False
        self.assertFalse(self.game.apply_move(22, -2))

    def test_apply_move_bear_off_ok_exacto(self):
        self.board.get_bar_count.return_value = 0
        self.dice.roll.return_value = (1, 4)
        self.game.roll()
        self.board.all_in_home.return_value = True
        self.board.bear_off_from.return_value = True
        self.assertTrue(self.game.apply_move(23, -2))
        self.assertEqual(self.pw.get_off_count(), 1)

    def test_apply_move_bear_off_overflow_true_y_false(self):
        self.board.get_bar_count.return_value = 0
        self.dice.roll.return_value = (6, 6)
        self.game.roll()
        self.board.all_in_home.return_value = True
        self.board.bear_off_from.return_value = True
        self.board.count_color_on_point.return_value = 0
        self.assertTrue(self.game.apply_move(20, -2))
        self.board.bear_off_from.return_value = False
        self.dice.roll.return_value = (6, 5)
        self.game.roll()
        self.assertFalse(self.game.apply_move(20, -2))

    def test_apply_move_normal_ok_y_fallas(self):
        self.board.get_bar_count.return_value = 0
        self.dice.roll.return_value = (3, 5)
        self.game.roll()
        self.assertFalse(self.game.apply_move(10, 9))
        self.assertFalse(self.game.apply_move(10, 10))
        self.board.move_on_board.return_value = True
        self.assertTrue(self.game.apply_move(10, 13))
        self.dice.roll.return_value = (6, 6)
        self.game.roll()
        self.board.move_on_board.return_value = False
        self.assertFalse(self.game.apply_move(5, 11))
        self.assertFalse(self.game.apply_move(5, 12))

    def test_has_winner(self):
        self.assertIsNone(self.game.has_winner())
        self.pw.add_off(15)
        self.assertIs(self.game.has_winner(), self.pw)
        self.pw._off = 0
        self.pb.add_off(15)
        self.assertIs(self.game.has_winner(), self.pb)

if __name__ == "__main__":
    unittest.main()
