import unittest
from unittest.mock import patch
from core.dice import Dice

class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_init_last_none(self):
        # Al inicio no hay tirada previa
        self.assertIsNone(self.dice.get_last())
        self.assertFalse(self.dice.is_double())

    @patch("random.randint", side_effect=[3, 5])
    def test_roll_not_double(self, mock_randint):
        result = self.dice.roll()
        self.assertEqual(result, (3, 5))
        self.assertEqual(self.dice.get_last(), (3, 5))
        self.assertFalse(self.dice.is_double())

    @patch("random.randint", side_effect=[4, 4])
    def test_roll_double(self, mock_randint):
        result = self.dice.roll()
        self.assertEqual(result, (4, 4))
        self.assertEqual(self.dice.get_last(), (4, 4))
        self.assertTrue(self.dice.is_double())
