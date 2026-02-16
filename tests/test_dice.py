import unittest
from unittest.mock import patch
from core.dice import Dice

class TestDice(unittest.TestCase):
    def setUp(self):
        self.d = Dice()

    def test_init_last_none(self):
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

    @patch("random.randint", side_effect=[1, 2, 3, 3, 4, 5])
    def test_last_updates_across_rolls_and_is_double_changes(self, _):
        self.assertEqual(self.d.roll(), (1, 2))
        self.assertEqual(self.d.get_last(), (1, 2))
        self.assertFalse(self.d.is_double())
        self.assertEqual(self.d.roll(), (3, 3))
        self.assertEqual(self.d.get_last(), (3, 3))
        self.assertTrue(self.d.is_double())
        self.assertEqual(self.d.roll(), (4, 5))
        self.assertEqual(self.d.get_last(), (4, 5))
        self.assertFalse(self.d.is_double())

    def test_reset_from_start_and_after_roll(self):
        self.d.reset()
        self.assertIsNone(self.d.get_last())
        self.assertFalse(self.d.is_double())
        with patch("random.randint", side_effect=[2, 4]):
            self.d.roll()
        self.assertIsNotNone(self.d.get_last())
        self.d.reset()
        self.assertIsNone(self.d.get_last())
        self.assertFalse(self.d.is_double())

    def test_multiple_instances_independent_state(self):
        d2 = Dice()
        with patch("random.randint", side_effect=[2, 2]):
            self.d.roll()
        with patch("random.randint", side_effect=[1, 6]):
            d2.roll()
        self.assertEqual(self.d.get_last(), (2, 2))
        self.assertEqual(d2.get_last(), (1, 6))
        self.assertTrue(self.d.is_double())
        self.assertFalse(d2.is_double())

    def test_is_double_truth_table(self):
        cases = [((1, 2), False), ((2, 2), True), ((5, 6), False), ((6, 6), True), ((3, 3), True)]
        seq = []
        for (x, y), _ in cases:
            seq.extend([x, y])
        with patch("random.randint", side_effect=seq):
            for (x, y), expected in cases:
                self.assertEqual(self.d.roll(), (x, y))
                self.assertEqual(self.d.is_double(), expected)

    @patch("random.randint", side_effect=[4, 1])
    def test_roll_return_equals_get_last_immediately(self, _):
        r = self.d.roll()
        self.assertEqual(r, self.d.get_last())

    def test_is_double_without_roll_and_after_reset(self):
        self.assertFalse(self.d.is_double())
        with patch("random.randint", side_effect=[5, 5]):
            self.d.roll()
        self.assertTrue(self.d.is_double())
        self.d.reset()
        self.assertFalse(self.d.is_double())

if __name__ == "__main__":
    unittest.main()
