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
        self.b.bear_off_from("white", 0) 
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
        self.assertIsNone(self.b.remove_from_bar("white"))  
        self.assertIsInstance(self.b.remove_from_bar("black"), Checker)
        self.assertIsNone(self.b.remove_from_bar("black"))

    def test_can_land_cases(self):
        self.b.clear()
        self.assertFalse(self.b.can_land(-1, "white"))
        self.assertFalse(self.b.can_land(24, "black"))
        self.assertTrue(self.b.can_land(0, "white"))  
        self.b.add_checker_to_point(1, "white")
        self.assertTrue(self.b.can_land(1, "white"))  
        self.b.clear()
        self.b.add_checker_to_point(2, "black")
        self.assertTrue(self.b.can_land(2, "white"))  
        self.b.add_checker_to_point(2, "black")
        self.assertFalse(self.b.can_land(2, "white"))  

 