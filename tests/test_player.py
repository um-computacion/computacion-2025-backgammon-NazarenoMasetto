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
        self.jugador.remove_from_bar(5)  
        self.assertEqual(self.jugador.get_bar_count(), 0)

    def test_agregar_fuera(self):
        self.jugador.add_off(4)
        self.assertEqual(self.jugador.get_off_count(), 4)
        self.jugador.add_off(1)
        self.assertEqual(self.jugador.get_off_count(), 5)

    def test_agregar_barra_valor_negativo(self):
        self.jugador.add_to_bar(-3)  
        self.assertEqual(self.jugador.get_bar_count(), 0)

    def test_quitar_barra_valor_negativo(self):
        self.jugador.add_to_bar(2)
        self.jugador.remove_from_bar(-1)  
        self.assertEqual(self.jugador.get_bar_count(), 2)

    def test_agregar_fuera_valor_negativo(self):
        self.jugador.add_off(-2)  
        self.assertEqual(self.jugador.get_off_count(), 0)

    def test_varios_movimientos(self):
        self.jugador.add_to_bar(2)
        self.jugador.add_off(1)
        self.assertEqual(self.jugador.get_bar_count(), 2)
        self.assertEqual(self.jugador.get_off_count(), 1)
        self.jugador.remove_from_bar(1)
        self.assertEqual(self.jugador.get_bar_count(), 1)

if __name__ == "__main__":
    unittest.main()
