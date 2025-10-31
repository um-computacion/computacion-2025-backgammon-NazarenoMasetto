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

    def test_apply_move_sin_dados_lanzados_devuelve_false(self):
        self.game.__rolled__ = False
        self.assertFalse(self.game.apply_move(0, 1))

    def test_apply_move_sin_movimientos_disponibles(self):
        self.game.__rolled__ = True
        self.game.__available__ = []
        self.assertFalse(self.game.apply_move(0, 1))

    def test_apply_move_desde_barra_destino_invalido(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.return_value = 1
        self.assertFalse(self.game.apply_move(-1, 10))

    def test_apply_move_excepcion_general_controlada(self):
        self.game.__rolled__ = True
        self.mock_board.get_bar_count.side_effect = Exception("Error simulado")
        self.assertFalse(self.game.apply_move(0, 1))

    def test_apply_move_bear_off_con_dado_mayor_exitoso(self):
        self.game.__rolled__ = True
        self.game.__turn_white__ = True
        self.game.__available__ = [6]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.count_color_on_point.return_value = 0
        self.mock_board.bear_off_from.return_value = True
        self.assertTrue(self.game.apply_move(23, -2))

    def test_apply_move_bear_off_con_dado_mayor_falla_por_fichas_detras(self):
        self.game.__rolled__ = True
        self.game.__available__ = [6]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "white"
        self.mock_board.count_color_on_point.side_effect = lambda i, c: 1 if i == 19 else 0
        self.assertFalse(self.game.apply_move(23, -2))

    def test_apply_move_movimiento_invalido_por_distancia(self):
        self.game.__rolled__ = True
        self.game.__available__ = [3]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.top_color_on_point.return_value = "white"
        self.assertFalse(self.game.apply_move(5, 3))

    def test_apply_move_movimiento_falla_por_consume(self):
        self.game.__rolled__ = True
        self.game.__available__ = [1]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.top_color_on_point.return_value = "white"
        self.assertFalse(self.game.apply_move(0, 3))

    def test_apply_move_bear_off_distancia_invalida(self):
        self.game.__rolled__ = True
        self.game.__available__ = [3]
        self.mock_board.get_bar_count.return_value = 0
        self.mock_board.all_in_home.return_value = True
        self.mock_board.top_color_on_point.return_value = "white"
        self.assertFalse(self.game.apply_move(10, -2))


if __name__ == "__main__":
    unittest.main()
