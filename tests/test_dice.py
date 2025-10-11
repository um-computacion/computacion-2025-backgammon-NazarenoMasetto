import unittest
from unittest.mock import patch
from core.dice import Dice

class TestDice(unittest.TestCase):
    def setUp(self):
        self.d = Dice()

    def test_init_last_none_and_is_double_false(self):
        self.assertIsNone(self.d.get_last())
        self.assertFalse(self.d.is_double())

    @patch("random.randint", side_effect=[3, 5])
    def test_roll_not_double(self, _):
        r = self.d.roll()
        self.assertEqual(r, (3, 5))
        self.assertEqual(self.d.get_last(), (3, 5))
        self.assertFalse(self.d.is_double())

    @patch("random.randint", side_effect=[6, 6])
    def test_roll_double(self, _):
        r = self.d.roll()
        self.assertEqual(r, (6, 6))
        self.assertEqual(self.d.get_last(), (6, 6))
        self.assertTrue(self.d.is_double())

    def test_roll_values_in_range_and_tuple_types(self):
        for _ in range(80):
            a, b = self.d.roll()
            self.assertTrue(1 <= a <= 6)
            self.assertTrue(1 <= b <= 6)
            self.assertIsInstance(self.d.get_last(), tuple)
            self.assertEqual(len(self.d.get_last()), 2)
            self.assertIsInstance(a, int)
            self.assertIsInstance(b, int)

    