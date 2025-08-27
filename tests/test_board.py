import unittest
from core.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.b = Board()

    def test_get_point_in_range(self):
        p0 = self.b.get_point(0)
        self.assertIsInstance(p0, list)
        self.assertEqual(len(p0), 0)
        p23 = self.b.get_point(23)
        self.assertIsInstance(p23, list)

    def test_get_point_out_of_range(self):
        self.assertIsNone(self.b.get_point(-1))
        self.assertIsNone(self.b.get_point(24))

    def test_add_checker_ok(self):
        ok = self.b.add_checker_to_point(5, "white")
        self.assertTrue(ok)
        p5 = self.b.get_point(5)
        self.assertEqual(len(p5), 1)
        self.assertEqual(p5[0].get_color(), "white")

    def test_add_checker_out_of_range(self):
        ok1 = self.b.add_checker_to_point(-1, "white")
        ok2 = self.b.add_checker_to_point(99, "black")
        self.assertFalse(ok1)
        self.assertFalse(ok2)
