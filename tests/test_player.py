import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.jugador = Player("Naza", "white")

    def test_crear_jugador(self):
        self.assertEqual(self.jugador.get_name(), "Naza")
        self.assertEqual(self.jugador.get_color(), "white")
        self.assertEqual(self.jugador.get_bar_count(), 0)
        self.assertEqual(self.jugador.get_off_count(), 0)

    def test_agregar_y_quitar_barra(self):
        self.jugador.add_to_bar(3)
        self.assertEqual(self.jugador.get_bar_count(), 3)
        self.jugador.remove_from_bar(2)
        self.assertEqual(self.jugador.get_bar_count(), 1)
        self.jugador.remove_from_bar(5)  # no puede quedar en negativo
        self.assertEqual(self.jugador.get_bar_count(), 0)