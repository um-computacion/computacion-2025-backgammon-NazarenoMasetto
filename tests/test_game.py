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
        # jugadores falsos
        self.pw = FakePlayer("W", "white")
        self.pb = FakePlayer("B", "black")

        # parches: reemplazamos Board y Dice dentro de core.game por mocks
        self.p_board = patch("core.game.Board")
        self.p_dice = patch("core.game.Dice")

        self.MockBoard = self.p_board.start()
        self.MockDice = self.p_dice.start()

        self.addCleanup(self.p_board.stop)
        self.addCleanup(self.p_dice.stop)

        # instancias mock como tablero y dados
        self.board = MagicMock()
        self.dice = MagicMock()

        self.MockBoard.return_value = self.board
        self.MockDice.return_value = self.dice

        # juego real pero inyectando esos mocks
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
        moves = self.game.get_available_moves()
        self.assertCountEqual(moves, [3, 5])

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

    def test_can_bear_off_white(self):
        self.board.count_color_on_point.return_value = 0

        self.assertTrue(self.game.can_bear_off_with("white", 23, 1))
        self.assertTrue(self.game.can_bear_off_with("white", 22, 3))

        def fake_count(idx, color):
            if color == "white" and idx == 20:
                return 1
            return 0
        self.board.count_color_on_point.side_effect = fake_count
        self.assertFalse(self.game.can_bear_off_with("white", 22, 5))

    def test_can_bear_off_black(self):
        self.board.count_color_on_point.return_value = 0

        self.assertTrue(self.game.can_bear_off_with("black", 0, 1))
        self.assertTrue(self.game.can_bear_off_with("black", 1, 3))

        def fake_count(idx, color):
            if color == "black" and idx == 4:
                return 1
            return 0
        self.board.count_color_on_point.side_effect = fake_count
        self.assertFalse(self.game.can_bear_off_with("black", 1, 5))

    def test_apply_move_rechazado_si_hay_bar_y_no_uso_bar(self):
        self.board.get_bar_count.return_value = 1
        self.dice.roll.return_value = (3, 4)
        self.game.roll()
        self.assertFalse(self.game.apply_move(5, 8))

    def test_apply_move_falla_sin_available_moves(self):
        self.board.get_bar_count.return_value = 0
        self.assertFalse(self.game.apply_move(5, 8))

    def test_apply_move_desde_bar_ok(self):
        self.board.get_bar_count.return_value = 1
        self.dice.roll.return_value = (2, 5)
        self.game.roll()

        self.board.move_from_bar.return_value = True
        dest_ok = self.game.entry_point_for_die("white", 2)

        self.assertTrue(self.game.apply_move(-1, dest_ok))
        self.assertFalse(self.game.apply_move(-1, 99))

    def test_apply_move_desde_bar_falla_por_board(self):
        self.board.get_bar_count.return_value = 1
        self.dice.roll.return_value = (3, 6)
        self.game.roll()

        self.board.move_from_bar.return_value = False
        dest_ok = self.game.entry_point_for_die("white", 3)
        self.assertFalse(self.game.apply_move(-1, dest_ok))

    def test_apply_move_bear_off_rechazado_si_no_all_in_home(self):
        self.board.get_bar_count.return_value = 0
        self.dice.roll.return_value = (2, 3)
        self.game.roll()

        self.board.all_in_home.return_value = False
        self.assertFalse(self.game.apply_move(22, -2))

    def test_apply_move_bear_off_ok(self):
        self.board.get_bar_count.return_value = 0
        self.dice.roll.return_value = (1, 4)
        self.game.roll()

        self.board.all_in_home.return_value = True
        self.board.bear_off_from.return_value = True

        self.assertTrue(self.game.apply_move(23, -2))
        self.assertEqual(self.pw.get_off_count(), 1)

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
        self.pb._off = 15
        self.assertIs(self.game.has_winner(), self.pb)


if __name__ == "__main__":
    unittest.main()
