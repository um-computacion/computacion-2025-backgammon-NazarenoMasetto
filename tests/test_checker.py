import unittest
from core.board import Board
from core.checker import Checker

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.b = Board()

    def test_get_point_in_range(self):
        self.assertIsInstance(self.b.get_point(0), list)
        self.assertIsInstance(self.b.get_point(23), list)

    def test_get_point_out_of_range(self):
        self.assertIsNone(self.b.get_point(-1))
        self.assertIsNone(self.b.get_point(24))

    def test_add_checker_ok(self):
        ok = self.b.add_checker_to_point(5, "white")
        self.assertTrue(ok)
        self.assertEqual(self.b.get_point(5)[0].get_color(), "white")

    def test_add_checker_out_of_range(self):
        self.assertFalse(self.b.add_checker_to_point(-1, "white"))
        self.assertFalse(self.b.add_checker_to_point(99, "black"))

    def test_pop_checker_ok_and_empty(self):
        self.b.add_checker_to_point(3, "black")
        ficha = self.b.pop_checker_from_point(3)
        self.assertIsInstance(ficha, Checker)
        self.assertIsNone(self.b.pop_checker_from_point(3))

    def test_pop_checker_out_of_range(self):
        self.assertIsNone(self.b.pop_checker_from_point(-1))
        self.assertIsNone(self.b.pop_checker_from_point(99))

    def test_top_color_on_point_ok_and_empty(self):
        self.b.add_checker_to_point(4, "white")
        self.assertEqual(self.b.top_color_on_point(4), "white")
        self.assertIsNone(self.b.top_color_on_point(5))

    def test_top_color_on_point_out_of_range(self):
        self.assertIsNone(self.b.top_color_on_point(-1))
        self.assertIsNone(self.b.top_color_on_point(25))

    def test_count_color_on_point(self):
        self.b.add_checker_to_point(6, "white")
        self.b.add_checker_to_point(6, "white")
        self.b.add_checker_to_point(6, "black")
        self.assertEqual(self.b.count_color_on_point(6, "white"), 2)
        self.assertEqual(self.b.count_color_on_point(6, "black"), 1)

    def test_count_color_on_point_out_of_range(self):
        self.assertEqual(self.b.count_color_on_point(-1, "white"), 0)
        self.assertEqual(self.b.count_color_on_point(99, "black"), 0)

    def test_setup_start_position_distribution(self):
        self.b.setup_start_position()
        self.assertEqual(len(self.b.get_point(0)), 2)
        self.assertEqual(len(self.b.get_point(23)), 2)
        self.assertEqual(len(self.b.get_point(11)), 5)
        self.assertEqual(len(self.b.get_point(12)), 5)
        self.assertEqual(len(self.b.get_point(16)), 3)
        self.assertEqual(len(self.b.get_point(7)), 3)
        self.assertEqual(len(self.b.get_point(18)), 5)
        self.assertEqual(len(self.b.get_point(5)), 5)

    def test_add_and_remove_from_bar(self):
        self.b.add_to_bar("white")
        self.assertEqual(self.b.get_bar_count("white"), 1)
        self.assertIsInstance(self.b.remove_from_bar("white"), Checker)
        self.assertIsNone(self.b.remove_from_bar("white"))

    def test_get_home_count(self):
        self.assertEqual(self.b.get_home_count("white"), 0)
        self.assertEqual(self.b.get_home_count("black"), 0)

    def test_can_land_conditions(self):
        self.assertTrue(self.b.can_land(3, "white"))
        self.assertFalse(self.b.can_land(-1, "white"))
        self.b.add_checker_to_point(2, "white")
        self.assertTrue(self.b.can_land(2, "white"))
        self.b.clear()
        self.b.add_checker_to_point(4, "black")
        self.assertTrue(self.b.can_land(4, "white"))
        self.b.add_checker_to_point(4, "black")
        self.assertFalse(self.b.can_land(4, "white"))

    def test_move_on_board_ok_and_fail(self):
        self.b.add_checker_to_point(0, "white")
        self.assertTrue(self.b.move_on_board("white", 0, 1))
        self.assertFalse(self.b.move_on_board("white", 0, 1))
        self.assertFalse(self.b.move_on_board("black", 1, 2))

    def test_bear_off_from_ok_and_fail(self):
        self.b.add_checker_to_point(10, "white")
        self.assertTrue(self.b.bear_off_from("white", 10))
        self.assertFalse(self.b.bear_off_from("white", 10))
        self.assertFalse(self.b.bear_off_from("white", -1))
        self.assertFalse(self.b.bear_off_from("black", 20))

if __name__ == "__main__":
    unittest.main()
