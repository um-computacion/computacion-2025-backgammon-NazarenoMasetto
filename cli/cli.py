from core.board import Board
from core.dice import Dice
from core.player import Player
from core.game import Game


class CLI:
    """
    Clase que representa la interfaz de línea de comandos (CLI) del juego Backgammon.

    Se encarga de gestionar la interacción entre el usuario y la lógica del juego
    implementada en la clase Game. Permite iniciar una partida, mostrar el estado
    actual del tablero, tirar los dados, ingresar movimientos y detectar el ganador.

    No implementa reglas del juego, sino que utiliza los métodos de la clase Game
    para ejecutar las acciones válidas según las reglas del Backgammon.
    """

    def __init__(self):
        self.__game__ = None

    def start_game(self):
        board = Board()
        dice = Dice()
        player_white = Player("Jugador Blanco", "white")
        player_black = Player("Jugador Negro", "black")
        self.__game__ = Game(board, dice, player_white, player_black)
        self.__game__.start()
        print("=== BACKGAMMON CLI ===")
        self.__show_board__()

        while True:
            player = self.__game__.current_player()
            print(f"\nTurno de: {player.get_name()} ({player.get_color()})")
            d1, d2 = self.__game__.roll()
            print(f"Dados: {d1} y {d2}")

            moves = self.__game__.get_available_moves()
            print(f"Movimientos disponibles: {moves}")

            src, dest = self.__ask_move__()
            if src == "salir":
                print("Saliendo del juego...")
                break

            if not self.__validate_input__(src, dest):
                print("Entrada inválida. Use números o 'salir'.")
                continue

            src, dest = int(src), int(dest)
            moved = self.__game__.apply_move(src, dest)

            if moved:
                print(f"Movimiento {src} -> {dest} realizado correctamente.")
            else:
                print(f"Movimiento {src} -> {dest} inválido.")

            winner = self.__game__.has_winner()
            if winner:
                print(f"🎉 ¡{winner.get_name()} ha ganado la partida! 🎉")
                break

            self.__game__.end_turn()
            self.__show_board__()

    def __ask_move__(self):
        entrada = input("Ingrese movimiento (src dest) o 'salir': ").strip()
        if entrada.lower() == "salir":
            return "salir", None
        partes = entrada.split()
        if len(partes) != 2:
            return None, None
        return partes[0], partes[1]

    def __validate_input__(self, src, dest):
        if src is None or dest is None:
            return False
        try:
            int(src)
            int(dest)
            return True
        except ValueError:
            return False

    def __show_board__(self):
        board = self.__game__.get_board()
        print("\nTablero simplificado:")
        linea = ""
        for i in range(24):
            punto = board.get_point(i)
            cantidad = len(punto)
            color = punto[-1].get_color()[0].upper() if cantidad > 0 else " "
            linea += f"{i:02d}[{cantidad}{color}] "
            if i == 11:
                linea += "\n"
        print(linea)
