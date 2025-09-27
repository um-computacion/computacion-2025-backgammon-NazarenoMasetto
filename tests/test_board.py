import unittest
from core.board import Board
from core.checker import Checker

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.b = Board()

    def test_get_point_valid_invalid(self):
        self.assertIsInstance(self.b.get_point(0), list)
        self.assertIsInstance(self.b.get_point(23), list)
        self.assertIsNone(self.b.get_point(-1))
        self.assertIsNone(self.b.get_point(24))

    def test_clear_resets_everything(self):
        self.b.add_checker_to_point(0, "white")
        self.b.add_to_bar("white")
        self.b.add_to_bar("black")
        self.b.bear_off_from("white", 0)  # no hará nada útil si no hay blanca arriba; no importa
        self.b.clear()
        for i in range(24):
            self.assertEqual(len(self.b.get_point(i)), 0)
        self.assertEqual(self.b.get_bar_count("white"), 0)
        self.assertEqual(self.b.get_bar_count("black"), 0)
        self.assertEqual(self.b.get_home_count("white"), 0)
        self.assertEqual(self.b.get_home_count("black"), 0)

    def test_setup_start_position_distribution(self):
        self.b.setup_start_position()
        self.assertEqual(self.b.count_color_on_point(0, "white"), 2)
        self.assertEqual(self.b.count_color_on_point(23, "black"), 2)
        self.assertEqual(self.b.count_color_on_point(11, "white"), 5)
        self.assertEqual(self.b.count_color_on_point(12, "black"), 5)
        self.assertEqual(self.b.count_color_on_point(16, "white"), 3)
        self.assertEqual(self.b.count_color_on_point(7,  "black"), 3)
        self.assertEqual(self.b.count_color_on_point(18, "white"), 5)
        self.assertEqual(self.b.count_color_on_point(5,  "black"), 5)

    def test_add_and_pop_checker(self):
        self.assertTrue(self.b.add_checker_to_point(5, "white"))
        self.assertIsInstance(self.b.top_color_on_point(5), str)
        self.assertEqual(self.b.top_color_on_point(5), "white")
        popped = self.b.pop_checker_from_point(5)
        self.assertIsInstance(popped, Checker)
        self.assertIsNone(self.b.top_color_on_point(5))
        self.assertIsNone(self.b.pop_checker_from_point(5))
        self.assertFalse(self.b.add_checker_to_point(-1, "white"))
        self.assertFalse(self.b.add_checker_to_point(99, "black"))
        self.assertIsNone(self.b.pop_checker_from_point(-1))
        self.assertIsNone(self.b.pop_checker_from_point(99))
        self.assertIsNone(self.b.top_color_on_point(-1))
        self.assertIsNone(self.b.top_color_on_point(99))

    def test_count_color_on_point(self):
        self.b.clear()
        self.assertEqual(self.b.count_color_on_point(-1, "white"), 0)
        self.assertEqual(self.b.count_color_on_point(99, "black"), 0)
        self.assertEqual(self.b.count_color_on_point(3, "white"), 0)
        self.b.add_checker_to_point(3, "white")
        self.b.add_checker_to_point(3, "black")
        self.b.add_checker_to_point(3, "white")
        self.assertEqual(self.b.count_color_on_point(3, "white"), 2)
        self.assertEqual(self.b.count_color_on_point(3, "black"), 1)

    def test_bar_and_home_basic(self):
        self.b.clear()
        self.assertEqual(self.b.get_bar_count("white"), 0)
        self.assertEqual(self.b.get_bar_count("black"), 0)
        self.assertEqual(self.b.get_home_count("white"), 0)
        self.assertEqual(self.b.get_home_count("black"), 0)
        self.b.add_to_bar("white")
        self.b.add_to_bar("black")
        self.assertEqual(self.b.get_bar_count("white"), 1)
        self.assertEqual(self.b.get_bar_count("black"), 1)
        self.assertIsInstance(self.b.remove_from_bar("white"), Checker)
        self.assertIsNone(self.b.remove_from_bar("white"))  # ya vacía
        self.assertIsInstance(self.b.remove_from_bar("black"), Checker)
        self.assertIsNone(self.b.remove_from_bar("black"))

    def test_can_land_cases(self):
        self.b.clear()
        self.assertFalse(self.b.can_land(-1, "white"))
        self.assertFalse(self.b.can_land(24, "black"))
        self.assertTrue(self.b.can_land(0, "white"))  # vacío
        self.b.add_checker_to_point(1, "white")
        self.assertTrue(self.b.can_land(1, "white"))  # misma color
        self.b.clear()
        self.b.add_checker_to_point(2, "black")
        self.assertTrue(self.b.can_land(2, "white"))  # 1 oponente: golpe
        self.b.add_checker_to_point(2, "black")
        self.assertFalse(self.b.can_land(2, "white"))  # 2 o más oponentes: bloqueado

    def test_move_from_bar_white_paths(self):
        self.b.clear()
        self.assertFalse(self.b.move_from_bar("white", -1))
        self.assertFalse(self.b.move_from_bar("white", 6))
        self.assertFalse(self.b.move_from_bar("white", 0))  # no hay en barra
        self.b.add_to_bar("white")
        self.assertTrue(self.b.move_from_bar("white", 0))   # aterriza vacío
        self.b.add_to_bar("white")
        self.b.add_checker_to_point(1, "black")
        self.assertTrue(self.b.move_from_bar("white", 1))   # golpea una negra sola
        self.b.add_to_bar("white")
        self.b.add_checker_to_point(2, "black")
        self.b.add_checker_to_point(2, "black")
        self.assertFalse(self.b.move_from_bar("white", 2))  # dos negras bloquean

    def test_move_from_bar_black_paths(self):
        self.b.clear()
        self.assertFalse(self.b.move_from_bar("black", 17))
        self.assertFalse(self.b.move_from_bar("black", 24))
        self.assertFalse(self.b.move_from_bar("black", 23))  # no hay en barra
        self.b.add_to_bar("black")
        self.assertTrue(self.b.move_from_bar("black", 23))   # aterriza vacío
        self.b.add_to_bar("black")
        self.b.add_checker_to_point(22, "white")
        self.assertTrue(self.b.move_from_bar("black", 22))   # golpea una blanca sola
        self.b.add_to_bar("black")
        self.b.add_checker_to_point(21, "white")
        self.b.add_checker_to_point(21, "white")
        self.assertFalse(self.b.move_from_bar("black", 21))  # dos blancas bloquean

    def test_move_on_board_paths(self):
        self.b.clear()
        self.assertFalse(self.b.move_on_board("white", -1, 0))
        self.assertFalse(self.b.move_on_board("white", 0, 24))
        self.assertFalse(self.b.move_on_board("white", 0, 1))  # origen vacío
        self.b.add_checker_to_point(0, "black")
        self.assertFalse(self.b.move_on_board("white", 0, 1))  # arriba no es blanca
        self.b.clear()
        self.b.add_checker_to_point(0, "white")
        self.b.add_checker_to_point(1, "black")
        self.b.add_checker_to_point(1, "black")
        self.assertFalse(self.b.move_on_board("white", 0, 1))  # dos negras bloquean
        self.b.clear()
        self.b.add_checker_to_point(0, "white")
        self.assertTrue(self.b.move_on_board("white", 0, 1))   # a vacío
        self.b.add_checker_to_point(2, "white")
        self.assertTrue(self.b.move_on_board("white", 2, 1))   # a misma color
        self.b.add_checker_to_point(3, "white")
        self.b.add_checker_to_point(4, "black")
        self.assertTrue(self.b.move_on_board("white", 3, 4))   # golpe a una sola

    def test_bear_off_from_paths(self):
        self.b.clear()
        self.assertFalse(self.b.bear_off_from("white", -1))
        self.assertFalse(self.b.bear_off_from("white", 24))
        self.assertFalse(self.b.bear_off_from("white", 0))  # vacío
        self.b.add_checker_to_point(0, "black")
        self.assertFalse(self.b.bear_off_from("white", 0))  # arriba no es blanca
        self.b.clear()
        self.b.add_checker_to_point(23, "white")
        self.assertTrue(self.b.bear_off_from("white", 23))
        self.assertEqual(self.b.get_home_count("white"), 1)
        self.b.clear()
        self.b.add_checker_to_point(0, "black")
        self.assertTrue(self.b.bear_off_from("black", 0))
        self.assertEqual(self.b.get_home_count("black"), 1)

    def test_all_in_home_true_false_white(self):
        self.b.clear()
        self.assertTrue(self.b.all_in_home("white"))  # no blancas fuera de 18..23 y sin barra
        self.b.add_checker_to_point(0, "white")
        self.assertFalse(self.b.all_in_home("white"))  # blanca fuera del home
        self.b.clear()
        self.b.add_to_bar("white")
        self.assertFalse(self.b.all_in_home("white"))  # hay en barra

    def test_all_in_home_true_false_black(self):
        self.b.clear()
        self.assertTrue(self.b.all_in_home("black"))  # no negras fuera de 0..5 y sin barra
        self.b.add_checker_to_point(23, "black")
        self.assertFalse(self.b.all_in_home("black"))  # negra fuera del home
        self.b.clear()
        self.b.add_to_bar("black")
        self.assertFalse(self.b.all_in_home("black"))  # hay en barra

if __name__ == "__main__":
    unittest.main()
