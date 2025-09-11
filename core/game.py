from .board import Board
from .dice import Dice
from .player import Player

class BackgammonGame:
    """
    Controla el juego de Backgammon.
    Maneja jugadores, tablero, dados y turnos.
    """

    def __init__(self, player_white, player_black):
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__players__ = (player_white, player_black)
        self.__turn_index__ = 0
        self.__available_moves__ = []
        self.__last_roll__ = None

    def start(self):
        """
        Prepara el tablero con la posición inicial estándar.
        """
        self.__board__.setup_start_position()

    def current_player(self):
        """
        Devuelve el jugador actual.
        """
        return self.__players__[self.__turn_index__]

    def other_player(self):
        """
        Devuelve el jugador contrario al actual.
        """
        if self.__turn_index__ == 0:
            return self.__players__[1]
        return self.__players__[0]

    def roll(self):
        """
        Tira los dados y genera los movimientos disponibles.
        Maneja el caso de dobles (4 movimientos).
        """
        resultado = self.__dice__.roll()
        self.__last_roll__ = resultado
        self.__available_moves__ = []
        d1 = resultado[0]
        d2 = resultado[1]
        if d1 == d2:
            i = 0
            while i < 4:
                self.__available_moves__.append(d1)
                i = i + 1
        else:
            self.__available_moves__.append(d1)
            self.__available_moves__.append(d2)
        return resultado

    def end_turn(self):
        """
        Cambia al siguiente jugador.
        """
        if self.__turn_index__ == 0:
            self.__turn_index__ = 1
        else:
            self.__turn_index__ = 0
        self.__available_moves__ = []
        self.__last_roll__ = None

    def get_board(self):
        return self.__board__

    def get_available_moves(self):
        copia = []
        i = 0
        while i < len(self.__available_moves__):
            copia.append(self.__available_moves__[i])
            i = i + 1
        return copia

    def consume_move_value(self, used):
        i = 0
        while i < len(self.__available_moves__):
            if self.__available_moves__[i] == used:
                self.__available_moves__.pop(i)
                return True
            i = i + 1
        return False

    def direction(self, color):
        if color == "white":
            return 1
        return -1

    def entry_point_for_die(self, color, die):
        if color == "white":
            return die - 1
        else:
            return 23 - (die - 1)

    def distance(self, color, src, dest):
        if color == "white":
            return dest - src
        else:
            return src - dest

    def can_bear_off_with(self, color, src, die):
        if color == "white":
            exacto = (src + die == 24)
            mayor = (src + die > 24)
            if exacto:
                return True
            if mayor:
                i = 18
                while i < src:
                    if self.__board__.count_color_on_point(i, "white") > 0:
                        return False
                    i = i + 1
                return True
            return False
        else:
            exacto = (src - die == -1)
            mayor = (src - die < -1)
            if exacto:
                return True
            if mayor:
                i = 5
                while i > src:
                    if self.__board__.count_color_on_point(i, "black") > 0:
                        return False
                    i = i - 1
                return True
            return False

    def apply_move(self, src, dest):
        """
        Aplica un movimiento para el jugador actual.
        src = -1 (desde barra)
        dest = -2 (bear-off)
        """
        jugador = self.current_player()
        color = jugador.get_color()

        if self.__board__.get_bar_count(color) > 0 and src != -1:
            return False
        if len(self.__available_moves__) == 0:
            return False

        if src == -1:
            i = 0
            while i < len(self.__available_moves__):
                die = self.__available_moves__[i]
                esperado = self.entry_point_for_die(color, die)
                if esperado == dest:
                    ok = self.__board__.move_from_bar(color, dest)
                    if ok:
                        self.__available_moves__.pop(i)
                        return True
                    else:
                        return False
                i = i + 1
            return False

        if dest == -2:
            if not self.__board__.all_in_home(color):
                return False
            i = 0
            while i < len(self.__available_moves__):
                die = self.__available_moves__[i]
                if self.can_bear_off_with(color, src, die):
                    ok = self.__board__.bear_off_from(color, src)
                    if ok:
                        self.__available_moves__.pop(i)
                        jugador.add_off(1)
                        return True
                    else:
                        return False
                i = i + 1
            return False
        else:
            paso = self.distance(color, src, dest)
            if paso <= 0:
                return False
            i = 0
            while i < len(self.__available_moves__):
                die = self.__available_moves__[i]
                if die == paso:
                    ok = self.__board__.move_on_board(color, src, dest)
                    if ok:
                        self.__available_moves__.pop(i)
                        return True
                    else:
                        return False
                i = i + 1
            return False

    def has_winner(self):
        if self.__players__[0].get_off_count() >= 15:
            return self.__players__[0]
        if self.__players__[1].get_off_count() >= 15:
            return self.__players__[1]
        return None
