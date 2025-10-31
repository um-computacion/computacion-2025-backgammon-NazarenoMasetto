import unittest
from unittest.mock import patch, MagicMock
from itertools import cycle
from cli.cli import CLI


class TestCLI(unittest.TestCase):
    """
    Tests de la clase CLI del juego Backgammon.
    Verifican la interacción con el usuario, la tirada de dados,
    los movimientos válidos e inválidos, la impresión del tablero
    y el flujo de turnos y ganador.
    """

    def setUp(self):
        self.cli = CLI()

    # ----------------------------
    # Inicialización y salida
    # ----------------------------
    @patch("builtins.print")
    def test_start_game_initialization(self, mock_print):
        with patch("builtins.input", side_effect=["salir"]):
            self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("BACKGAMMON CLI", salida)

    @patch("builtins.input", side_effect=["salir"])
    @patch("builtins.print")
    def test_salir_inmediatamente(self, mock_print, mock_input):
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Saliendo del juego", salida)

    # ----------------------------
    # Movimientos y validaciones
    # ----------------------------
    @patch("core.dice.Dice.roll", return_value=(3, 5))
    @patch("builtins.input", side_effect=["0 3", "salir"])
    @patch("builtins.print")
    def test_movimiento_valido(self, mock_print, mock_input, mock_roll):
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Movimiento", salida)

    @patch("core.dice.Dice.roll", return_value=(3, 5))
    @patch("builtins.input", side_effect=["x y", "salir"])
    @patch("builtins.print")
    def test_movimiento_invalido_por_input(self, mock_print, mock_input, mock_roll):
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Entrada inválida", salida)

    @patch("core.dice.Dice.roll", return_value=(2, 2))
    @patch("builtins.input", side_effect=["salir"])
    @patch("builtins.print")
    def test_tirada_doble(self, mock_print, mock_input, mock_roll):
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Dados: 2 y 2", salida)

    @patch("core.dice.Dice.roll", return_value=(1, 6))
    @patch("builtins.input", side_effect=["0 6", "salir"])
    @patch("builtins.print")
    def test_mostrar_tablero_llamado(self, mock_print, mock_input, mock_roll):
        self.cli.start_game()
        llamado = any("Tablero simplificado" in str(c) for c in mock_print.call_args_list)
        self.assertTrue(llamado)

    @patch("core.dice.Dice.roll", return_value=(3, 5))
    @patch("builtins.input", side_effect=["0 3", "salir"])
    @patch("builtins.print")
    def test_termina_sin_ganador(self, mock_print, mock_input, mock_roll):
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertNotIn("ha ganado", salida)

    # ----------------------------
    # Nuevos casos extendidos
    # ----------------------------
    @patch("core.game.Game.has_winner", return_value=None)
    @patch("core.dice.Dice.roll", side_effect=cycle([(1, 2), (3, 4), (5, 6)]))
    @patch("builtins.input", side_effect=["0 2", "1 5", "salir"])
    @patch("builtins.print")
    def test_varios_turnos(self, mock_print, mock_input, mock_roll, mock_win):
        """Simula dos turnos seguidos y verifica impresión de ambos."""
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Turno de:", salida)

    @patch("core.game.Game.has_winner")
    @patch("core.dice.Dice.roll", return_value=(4, 3))
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["0 3", "salir"])
    def test_ganador_detectado(self, mock_input, mock_print, mock_roll, mock_win):
        """Verifica mensaje de victoria cuando has_winner devuelve jugador."""
        jugador_mock = MagicMock()
        jugador_mock.get_name.return_value = "Joaco"
        mock_win.side_effect = [jugador_mock, jugador_mock]
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Joaco ha ganado", salida)

    @patch("core.dice.Dice.roll", return_value=(5, 6))
    @patch("builtins.input", side_effect=["", "salir"])
    @patch("builtins.print")
    def test_entrada_vacia(self, mock_print, mock_input, mock_roll):
        """Prueba que una entrada vacía muestre mensaje de error."""
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Entrada inválida", salida)

    @patch("core.dice.Dice.roll", side_effect=[(1, 2), (4, 6)])
    @patch("builtins.input", side_effect=["0 1", "salir"])
    @patch("builtins.print")
    def test_roll_diferentes_valores(self, mock_print, mock_input, mock_roll):
        """Verifica que los valores de los dados cambian entre turnos."""
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Dados:", salida)

    @patch("core.dice.Dice.roll", return_value=(3, 5))
    @patch("builtins.input", side_effect=["0 3", "salir"])
    @patch("builtins.print")
    def test_mostrar_tablero_despues_movimiento(self, mock_print, mock_input, mock_roll):
        """Verifica que el tablero se muestre luego de un movimiento."""
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Tablero simplificado", salida)

    @patch("core.dice.Dice.roll", return_value=(4, 6))
    @patch("builtins.input", side_effect=["0 6", "salir"])
    @patch("builtins.print")
    def test_fin_del_turno_muestra_tablero(self, mock_print, mock_input, mock_roll):
        """Comprueba que se muestra el tablero tras end_turn()."""
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Tablero simplificado", salida)

    # ----------------------------
    # Tests adicionales (cantidad)
    # ----------------------------
    @patch("builtins.input", side_effect=["salir"])
    @patch("builtins.print")
    def test_inicio_muestra_tablero(self, mock_print, mock_input):
        """Verifica que el tablero se muestre al iniciar el juego."""
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Tablero simplificado", salida)

    @patch("core.dice.Dice.roll", return_value=(2, 3))
    @patch("builtins.input", side_effect=["0 3 4", "salir"])
    @patch("builtins.print")
    def test_input_incorrecto_formato(self, mock_print, mock_input, mock_roll):
        """Verifica que se detecte formato incorrecto de movimiento."""
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Entrada inválida", salida)

    @patch("core.dice.Dice.roll", return_value=(1, 4))
    @patch("builtins.input", side_effect=["   0   4   ", "salir"])
    @patch("builtins.print")
    def test_input_espacios_extra(self, mock_print, mock_input, mock_roll):
        """Verifica que se puedan procesar entradas con espacios adicionales."""
        self.cli.start_game()
        salida = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Movimiento", salida)

    @patch("builtins.input", side_effect=["salir"])
    @patch("builtins.print")
    def test_juego_finaliza_correctamente(self, mock_print, mock_input):
        """Verifica que el juego termine cuando el jugador escribe 'salir'."""
        self.cli.start_game()
        llamadas = [str(c) for c in mock_print.call_args_list]
        self.assertTrue(any("Saliendo del juego" in s for s in llamadas))


if __name__ == "__main__":
    unittest.main()
