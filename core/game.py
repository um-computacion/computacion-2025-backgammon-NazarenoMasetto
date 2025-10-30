from core.board import Board
from core.dice import Dice
from core.player import Player


class Game:
    def __init__(self, board: Board, dice: Dice, player_white: Player, player_black: Player):
        self.__board__ = board
        self.__dice__ = dice
        self.__white__ = player_white
        self.__black__ = player_black
        self.__turn_white__ = True
        self.__available__ = []
        self.__rolled__ = False

    # -----------------------------
    # Control general
    # -----------------------------
    def start(self):
        self.__board__.setup_start_position()
        self.__turn_white__ = True
        self.__available__ = []
        self.__rolled__ = False

    def current_player(self):
        return self.__white__ if self.__turn_white__ else self.__black__

    def other_player(self):
        return self.__black__ if self.__turn_white__ else self.__white__

    def get_board(self):
        return self.__board__

    def get_available_moves(self):
        copia = []
        for v in self.__available__:
            copia.append(v)
        return copia

    def roll(self):
        d1, d2 = self.__dice__.roll()
        if d1 == d2:
            self.__available__ = [d1, d1, d1, d1]
        else:
            self.__available__ = [d1, d2]
        self.__rolled__ = True
        return (d1, d2)

    def end_turn(self):
        self.__turn_white__ = not self.__turn_white__
        self.__available__ = []
        self.__rolled__ = False

    # -----------------------------
    # Métodos internos
    # -----------------------------
    def __consume_exact__(self, val):
        if val in self.__available__:
            self.__available__.remove(val)
            return True
        return False

    def __consume_min_ge__(self, val):
        posibles = [v for v in self.__available__ if v >= val]
        if not posibles:
            return False
        elegido = min(posibles)
        self.__available__.remove(elegido)
        return True

    def __distance_board__(self, color, src, dest):
        if color == "white":
            if dest <= src:
                return -1
            return dest - src
        else:
            if dest >= src:
                return -1
            return src - dest

    def __distance_bar_enter__(self, color, dest):
        if color == "white":
            if 0 <= dest <= 5:
                return dest + 1
            return -1
        else:
            if 18 <= dest <= 23:
                return 24 - dest
            return -1

    def __distance_bear_off__(self, color, src):
        if color == "white":
            if 18 <= src <= 23:
                return 24 - src
            return -1
        else:
            if 0 <= src <= 5:
                return src + 1
            return -1

    def __there_is_behind_in_home__(self, color, src):
        if color == "white":
            for i in range(18, src):
                if self.__board__.count_color_on_point(i, "white") > 0:
                    return True
            return False
        else:
            for i in range(src + 1, 6):
                if self.__board__.count_color_on_point(i, "black") > 0:
                    return True
            return False

    def has_winner(self):
        if self.__board__.get_home_count("white") == 15:
            return self.__white__
        if self.__board__.get_home_count("black") == 15:
            return self.__black__
        return None

    # -----------------------------
    # Movimiento principal
    # -----------------------------
    def apply_move(self, src, dest):
        if not self.__rolled__:
            return False
        try:
            color = "white" if self.__turn_white__ else "black"

            # Sin dados disponibles
            if len(self.__available__) == 0:
                return False

            # Desde barra
            if self.__board__.get_bar_count(color) > 0:
                if src != -1:
                    return False
                dist = self.__distance_bar_enter__(color, dest)
                if dist == -1:
                    return False
                if not self.__consume_exact__(dist) and not self.__consume_min_ge__(dist):
                    return False
                return self.__board__.move_from_bar(color, dest)

            # Movimiento dentro del tablero
            if 0 <= src <= 23 and 0 <= dest <= 23:
                top = self.__board__.top_color_on_point(src)
                if top != color:
                    return False
                dist = self.__distance_board__(color, src, dest)
                if dist == -1:
                    return False
                if not self.__consume_exact__(dist) and not self.__consume_min_ge__(dist):
                    return False
                return self.__board__.move_on_board(color, src, dest)

            # Bear off
            if dest < 0 or dest > 23:
                if not self.__board__.all_in_home(color):
                    return False
                top = self.__board__.top_color_on_point(src)
                if top != color:
                    return False
                dist = self.__distance_bear_off__(color, src)
                if dist == -1:
                    return False
                # Exacto
                if self.__consume_exact__(dist):
                    return self.__board__.bear_off_from(color, src)
                # Dado mayor sin fichas detrás
                if not self.__there_is_behind_in_home__(color, src):
                    if self.__consume_min_ge__(dist):
                        return self.__board__.bear_off_from(color, src)
                return False

        except Exception:
            return False
