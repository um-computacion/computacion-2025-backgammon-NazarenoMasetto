import unittest
from unittest.mock import patch
from core.dice import Dice

class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_init_last_is_none(self):
        self.assertIsNone(self.dice.get_last())
        self.assertFalse(self.dice.is_double())

    @patch("random.randint", side_effect=[3, 5])
    def test_roll_not_double(self, _):
        result = self.dice.roll()
        self.assertEqual(result, (3, 5))
        self.assertEqual(self.dice.get_last(), (3, 5))
        self.assertFalse(self.dice.is_double())

    @patch("random.randint", side_effect=[6, 6])
    def test_roll_double(self, _):
        result = self.dice.roll()
        self.assertEqual(result, (6, 6))
        self.assertEqual(self.dice.get_last(), (6, 6))
        self.assertTrue(self.dice.is_double())

    def test_get_last_without_roll(self):
        self.assertIsNone(self.dice.get_last())

    def test_is_double_without_roll(self):
        self.assertFalse(self.dice.is_double())
