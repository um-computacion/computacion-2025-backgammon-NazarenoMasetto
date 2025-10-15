import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.pw = Player("Alice", "white")
        self.pb = Player("Bob", "black")

    def test_init_and_getters(self):
        self.assertEqual(self.pw.get_name(), "Alice")
        self.assertEqual(self.pw.get_color(), "white")
        self.assertEqual(self.pw.get_bar_count(), 0)
        self.assertEqual(self.pw.get_off_count(), 0)
        self.assertEqual(self.pb.get_name(), "Bob")
        self.assertEqual(self.pb.get_color(), "black")
        self.assertEqual(self.pb.get_bar_count(), 0)
        self.assertEqual(self.pb.get_off_count(), 0)

    def test_add_to_bar_positive_zero_negative(self):
        self.pw.add_to_bar(3)
        self.assertEqual(self.pw.get_bar_count(), 3)
        self.pw.add_to_bar(0)
        self.assertEqual(self.pw.get_bar_count(), 3)
        self.pw.add_to_bar(-2)
        self.assertEqual(self.pw.get_bar_count(), 3)