import unittest
from core.checker import Checker

class TestChecker(unittest.TestCase):

    def test_color_blanco(self):
        c = Checker("white")
        self.assertEqual(c.get_color(), "white")

    def test_color_negro(self):
        c = Checker("black")
        self.assertEqual(c.get_color(), "black")

    def test_color_cadena_inesperada(self):
        c = Checker("rojo")
        self.assertEqual(c.get_color(), "rojo")

    
    def test_independencia_de_instancias(self):
        c1 = Checker("white")
        c2 = Checker("black")
        self.assertEqual(c1.get_color(), "white")
        self.assertEqual(c2.get_color(), "black")
        self.assertNotEqual(c1.get_color(), c2.get_color())

  