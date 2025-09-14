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

    def test_count_color_ok_mixed(self):
        self.b.add_checker_to_point(3, "white")
        self.b.add_checker_to_point(3, "black")
        self.b.add_checker_to_point(3, "white")
        self.assertEqual(self.b.count_color_on_point(3, "white"), 2)
        self.assertEqual(self.b.count_color_on_point(3, "black"), 1)

    def test_count_color_out_of_range_and_empty(self):
        self.assertEqual(self.b.count_color_on_point(-5, "white"), 0)
        self.assertEqual(self.b.count_color_on_point(100, "black"), 0)
        self.assertEqual(self.b.count_color_on_point(10, "white"), 0)

    def test_setup_start_position(self):
        # Preparamos el board con fichas random
        self.b.add_checker_to_point(0, "black")
        self.b.add_checker_to_point(23, "white")
        self.b.add_checker_to_point(5, "white")

        # Ejecutamos setup
        self.b.setup_start_position()

        # Verificamos que todos los puntos existan y sean listas
        for i in range(24):
            self.assertIsInstance(self.b.get_point(i), list)

        # Verificamos las posiciones iniciales que sí son seguras de comprobar
        self.assertEqual(self.b.count_color_on_point(0, "white"), 2)
        self.assertEqual(self.b.count_color_on_point(23, "black"), 2)

if __name__ == "__main__":
    unittest.main()
