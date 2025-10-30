import unittest
from unittest.mock import Mock
from core.game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.mock_board = Mock()
        self.mock_dice = Mock()
        self.mock_white = Mock()
        self.mock_black = Mock()
        self.game = Game(self.mock_board, self.mock_dice, self.mock_white, self.mock_black)

    def test_inicializacion_y_getters(self):
        self.assertTrue(self.game.__turn_white__)
        self.assertEqual(self.game.get_board(), self.mock_board)
        self.assertEqual(self.game.current_player(), self.mock_white)
        self.assertEqual(self.game.other_player(), self.mock_black)

    def test_start_reinicia_estado(self):
        self.game.__available__ = [1, 2]
        self.game.__rolled__ = True
        self.game.start()
        self.assertEqual(self.game.__available__, [])
        self.assertFalse(self.game.__rolled__)
        self.assertTrue(self.game.__turn_white__)

    def test_roll_con_dados_distintos(self):
        self.mock_dice.roll.return_value = (3, 5)
        resultado = self.game.roll()
        self.assertEqual(resultado, (3, 5))
        self.assertEqual(self.game.__available__, [3, 5])
        self.assertTrue(self.game.__rolled__)

    def test_roll_con_doble(self):
        self.mock_dice.roll.return_value = (4, 4)
        resultado = self.game.roll()
        self.assertEqual(resultado, (4, 4))
        self.assertEqual(self.game.__available__, [4, 4, 4, 4])
        self.assertTrue(self.game.__rolled__)

    def test_end_turn_cambia_turno_y_resetea_estado(self):
        turno_inicial = self.game.__turn_white__
        self.game.end_turn()
        self.assertNotEqual(self.game.__turn_white__, turno_inicial)
        self.assertEqual(self.game.__available__, [])
        self.assertFalse(self.game.__rolled__)

    def test_get_available_moves_devuelve_copia(self):
        self.game.__available__ = [2, 3]
        copia = self.game.get_available_moves()
        self.assertEqual(copia, [2, 3])
        self.assertNotEqual(id(copia), id(self.game.__available__))

    def test_consume_exact_elimina_valor(self):
        self.game.__available__ = [4, 5]
        self.assertTrue(self.game.__consume_exact__(4))
        self.assertEqual(self.game.__available__, [5])

    def test_consume_exact_no_existe_valor(self):
        self.game.__available__ = [3]
        self.assertFalse(self.game.__consume_exact__(5))
        self.assertEqual(self.game.__available__, [3])

    def test_consume_min_ge_elimina_valor_mas_cercano(self):
        self.game.__available__ = [3, 6]
        self.assertTrue(self.game.__consume_min_ge__(4))
        self.assertEqual(self.game.__available__, [3])

    def test_consume_min_ge_sin_valor_valido(self):
        self.game.__available__ = [2, 3]
        self.assertFalse(self.game.__consume_min_ge__(6))
        self.assertEqual(self.game.__available__, [2, 3])

    def test_distance_board_white_y_black(self):
        self.assertEqual(self.game.__distance_board__("white", 2, 5), 3)
        self.assertEqual(self.game.__distance_board__("black", 5, 2), 3)
        self.assertEqual(self.game.__distance_board__("white", 5, 2), -1)
        self.assertEqual(self.game.__distance_board__("black", 2, 5), -1)

    def test_distance_bar_enter_white_y_black(self):
        self.assertEqual(self.game.__distance_bar_enter__("white", 3), 4)
        self.assertEqual(self.game.__distance_bar_enter__("black", 20), 4)
        self.assertEqual(self.game.__distance_bar_enter__("white", 10), -1)
        self.assertEqual(self.game.__distance_bar_enter__("black", 5), -1)

    def test_distance_bear_off_white_y_black(self):
        self.assertEqual(self.game.__distance_bear_off__("white", 20), 4)
        self.assertEqual(self.game.__distance_bear_off__("black", 4), 5)

    def test_there_is_behind_in_home_true_y_false(self):
        self.mock_board.count_color_on_point.side_effect = lambda i, c: 1 if i == 19 and c == "white" else 0
        self.assertTrue(self.game.__there_is_behind_in_home__("white", 21))

        self.mock_board.count_color_on_point.side_effect = lambda i, c: 1 if i == 4 and c == "black" else 0
        self.assertTrue(self.game.__there_is_behind_in_home__("black", 2))

        self.mock_board.count_color_on_point.return_value = 0
        self.assertFalse(self.game.__there_is_behind_in_home__("white", 21))

    def test_has_winner_blanco(self):
        self.mock_board.get_home_count.side_effect = lambda c: 15 if c == "white" else 0
        self.assertEqual(self.game.has_winner(), self.mock_white)

    def test_has_winner_negro(self):
        self.mock_board.get_home_count.side_effect = lambda c: 15 if c == "black" else 0
        self.assertEqual(self.game.has_winner(), self.mock_black)

    def test_has_winner_sin_ganador(self):
        self.mock_board.get_home_count.return_value = 0
        self.assertIsNone(self.game.has_winner())

    def test_apply_move_barra_invalido(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 1
        self.assertFalse(self.game.apply_move(0, 1))

    def test_apply_move_barra_exitoso(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 1
        self.mock_board.move_from_bar.return_value = True
        self.game.__available__ = [3]
        self.assertTrue(self.game.apply_move(-1, 2))

    def test_apply_move_ok_en_tablero(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.move_on_board.return_value = True
        self.game.__available__ = [1]
        self.assertTrue(self.game.apply_move(0, 1))

    def test_apply_move_bear_off_todo_ok(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.bear_off_from.return_value = True
        self.game.__available__ = [4]
        self.assertTrue(self.game.apply_move(20, -2))

    def test_apply_move_bear_off_falla(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.bear_off_from.return_value = False
        self.game.__available__ = [4]
        self.assertFalse(self.game.apply_move(20, -2))

    def test_apply_move_bear_off_fuera_de_home(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = False
        self.assertFalse(self.game.apply_move(20, -2))

    def test_apply_move_bear_off_color_incorrecto(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "black"
        self.assertFalse(self.game.apply_move(20, -2))

    def test_apply_move_fuera_de_rango(self):
        self.game.__rolled__ = True
        self.assertFalse(self.game.apply_move(999, 1))

    def test_apply_move_color_incorrecto(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.top_color_on_point.return_value = "black"
        self.assertFalse(self.game.apply_move(0, 1))

    def test_apply_move_sin_color_en_origen(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.top_color_on_point.return_value = None
        self.assertFalse(self.game.apply_move(0, 1))

    def test_apply_move_sin_roll_devuelve_false(self):
        self.game.__rolled__ = False
        self.assertFalse(self.game.apply_move(0, 1))

    def test_consume_exact_valor_duplicado(self):
        # Cubre caso con valores repetidos
        self.game.__available__ = [3, 3, 5]
        self.assertTrue(self.game.__consume_exact__(3))
        self.assertEqual(self.game.__available__, [3, 5])

    def test_consume_min_ge_con_varios_valores_validos(self):
        # Cubre búsqueda del valor más cercano mayor o igual
        self.game.__available__ = [2, 4, 6]
        self.assertTrue(self.game.__consume_min_ge__(3))
        self.assertEqual(self.game.__available__, [2, 6])

  
    def test_distance_bar_enter_fuera_de_rango(self):
        # Cubre caso de punto inválido
        self.assertEqual(self.game.__distance_bar_enter__("white", 30), -1)
        self.assertEqual(self.game.__distance_bar_enter__("black", -1), -1)

  
    def test_there_is_behind_in_home_false_ambos_colores(self):
        # Cubre caso sin fichas detrás
        self.mock_board.count_color_on_point.return_value = 0
        self.assertFalse(self.game.__there_is_behind_in_home__("white", 22))
        self.assertFalse(self.game.__there_is_behind_in_home__("black", 1))

    def test_apply_move_min_ge_sin_valor_valido(self):
        # Cubre rama donde no hay valor >= dado
        self.game.__available__ = [1, 2]
        self.assertFalse(self.game.__consume_min_ge__(5))
        self.assertEqual(self.game.__available__, [1, 2])

    def test_end_turn_varias_veces(self):
        # Cubre alternancia de turnos
        estado_inicial = self.game.__turn_white__
        for _ in range(3):
            self.game.end_turn()
        self.assertNotEqual(self.game.__turn_white__, estado_inicial)

    def test_distance_board_negativo_y_cero(self):
        # Distancia negativa o cero según posiciones
        # En el código real devuelve -1 cuando origen y destino son iguales
        self.assertEqual(self.game.__distance_board__("white", 5, 5), -1)
        self.assertLess(self.game.__distance_board__("white", 6, 3), 0)
        self.assertLess(self.game.__distance_board__("black", 3, 6), 0)

    def test_distance_bear_off_invalido(self):
        # Casos fuera del rango del tablero devuelven valores negativos
        self.assertLess(self.game.__distance_bear_off__("white", 30), 0)
        self.assertLess(self.game.__distance_bear_off__("black", -5), 0)

    def test_apply_move_color_incorrecto(self):
        self.game._Game__turn_white__ = True
        self.mock_board.top_color_on_point.return_value = "black"
        self.mock_board.move_on_board.return_value = True
        self.game._Game__rolled__ = True
        self.game._Game__available__ = [3]
        result = self.game.apply_move(0, 1)
        self.assertFalse(result)

    def test_apply_move_sin_tiro_previo(self):
        self.game._Game__rolled__ = False
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.move_on_board.return_value = True
        self.assertFalse(self.game.apply_move(0, 1))

    def test_apply_move_falla_general(self):
        # Simula un fallo inesperado durante el movimiento
        self.game._Game__rolled__ = True
        self.mock_board.move_on_board.side_effect = Exception("error simulado")
        resultado = self.game.apply_move(0, 1)
        self.assertFalse(resultado)

    def test_apply_move_sin_disponibles(self):
        """Cubre el caso donde no hay movimientos disponibles."""
        self.game._Game__rolled__ = True
        self.game._Game__available__ = []  # vacía
        self.assertFalse(self.game.apply_move(0, 1))

    def test_apply_move_en_tablero_falla_por_move_on_board(self):
        """Simula fallo de move_on_board devolviendo False."""
        self.game._Game__rolled__ = True
        self.game._Game__available__ = [3]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.move_on_board.return_value = False  # fuerza el fallo
        result = self.game.apply_move(0, 3)
        self.assertFalse(result)

    def test_apply_move_sin_tirar_dados(self):
        """Cubre el caso en que no se tiraron los dados antes de mover."""
        self.game._Game__rolled__ = False
        self.game._Game__available__ = [3]
        self.assertFalse(self.game.apply_move(0, 1))

    def test_apply_move_dest_fuera_de_rango(self):
        """Cubre el caso de destino fuera de rango (dest < 0 o dest > 23)."""
        self.game._Game__rolled__ = True
        self.game._Game__available__ = [4]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.top_color_on_point.return_value = "white"
        # Destino fuera del rango permitido
        self.assertFalse(self.game.apply_move(0, 24))

    def test_apply_move_fuera_de_rango_y_color_invalido(self):
        """Cubre src/dest fuera de rango y color incorrecto."""
        self.game._Game__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.top_color_on_point.return_value = "black"  # color incorrecto
        self.assertFalse(self.game.apply_move(0, 24))  # dest fuera de rango
        self.assertFalse(self.game.apply_move(-1, 2))  # src fuera de rango

    def test_apply_move_bear_off_invalido(self):
        """Cubre bear off rechazado por no estar todo en home o color distinto."""
        self.game._Game__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = False
        self.assertFalse(self.game.apply_move(20, -2))  # no puede bear off
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "black"
        self.assertFalse(self.game.apply_move(20, -2))  # color incorrecto

    def test_apply_move_move_on_board_falla(self):
        """Cubre caso donde move_on_board devuelve False."""
        self.game._Game__rolled__ = True
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.move_on_board.return_value = False
        self.game._Game__available__ = [2]
        self.assertFalse(self.game.apply_move(0, 2))

    def test_apply_move_bear_off_con_dado_mayor(self):
        """Cubre bear off usando dado mayor cuando no hay fichas atrás."""
        self.game._Game__rolled__ = True
        self.game._Game__turn_white__ = True
        self.game._Game__available__ = [6]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.count_color_on_point.return_value = 0
        self.mock_board.bear_off_from.return_value = True
        self.assertTrue(self.game.apply_move(23, -2))

    def test_apply_move_bear_off_con_dado_mayor_pero_hay_fichas_atras(self):
        """Rechaza bear off con dado mayor si hay fichas detrás."""
        self.game._Game__rolled__ = True
        self.game._Game__available__ = [6]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.count_color_on_point.side_effect = lambda i, c: 1 if i == 19 else 0
        self.assertFalse(self.game.apply_move(20, -2))

    def test_apply_move_bear_off_falla_despues_consume_min_ge(self):
        """Cubre el caso donde bear_off_from falla tras consumir con min_ge."""
        self.game._Game__rolled__ = True
        self.game._Game__available__ = [6]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.count_color_on_point.return_value = 0
        self.mock_board.bear_off_from.return_value = False
        self.assertFalse(self.game.apply_move(23, -2))
        self.assertIn(1, self.game._Game__available__)


if __name__ == "__main__":
    unittest.main()