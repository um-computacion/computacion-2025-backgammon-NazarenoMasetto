import unittest
from unittest.mock import patch
from core.dice import Dice

class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_init_last_none(self):
        self.assertIsNone(self.dice.get_last())
        self.assertFalse(self.dice.is_double())

    @patch("random.randint", side_effect=[3, 5])
    def test_roll_not_double(self, _):
        result = self.dice.roll()
        self.assertEqual(result, (3, 5))
        self.assertEqual(self.dice.get_last(), (3, 5))
        self.assertFalse(self.dice.is_double())

    @patch("random.randint", side_effect=[4, 4])
    def test_roll_double(self, _):
        result = self.dice.roll()
        self.assertEqual(result, (4, 4))
        self.assertEqual(self.dice.get_last(), (4, 4))
        self.assertTrue(self.dice.is_double())

    def test_get_last_without_roll(self):
        self.assertIsNone(self.dice.get_last())

    def test_is_double_without_roll(self):
        self.assertFalse(self.dice.is_double())

    def test_values_always_in_range(self):
        for _ in range(50):
            d1, d2 = self.dice.roll()
            self.assertTrue(1 <= d1 <= 6)
            self.assertTrue(1 <= d2 <= 6)
            self.assertIsNotNone(self.dice.get_last())

    @patch("random.randint", side_effect=[1, 1, 2, 3, 6, 6])
    def test_last_updates_across_rolls(self, _):
        self.assertEqual(self.dice.roll(), (1, 1))
        self.assertEqual(self.dice.get_last(), (1, 1))
        self.assertTrue(self.dice.is_double())
        self.assertEqual(self.dice.roll(), (2, 3))
        self.assertEqual(self.dice.get_last(), (2, 3))
        self.assertFalse(self.dice.is_double())
        self.assertEqual(self.dice.roll(), (6, 6))
        self.assertEqual(self.dice.get_last(), (6, 6))
        self.assertTrue(self.dice.is_double())

    def test_tuple_and_types(self):
        d1, d2 = self.dice.roll()
        self.assertIsInstance(d1, int)
        self.assertIsInstance(d2, int)
        self.assertEqual(len(self.dice.get_last()), 2)

    def test_is_double_truth_table(self):
        cases = [((1, 2), False), ((2, 2), True), ((3, 5), False), ((6, 6), True)]
        seq = []
        for (a, b), _ in cases:
            seq.extend([a, b])
        with patch("random.randint", side_effect=seq):
            for (a, b), expected in cases:
                self.assertEqual(self.dice.roll(), (a, b))
                self.assertEqual(self.dice.is_double(), expected)

if __name__ == "__main__":
    unittest.main()
