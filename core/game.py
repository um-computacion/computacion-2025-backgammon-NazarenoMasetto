class Game:
    def __init__(self, board, dice, player_white, player_black):
        self.__board__ = board
        self.__dice__ = dice
        self.__white__ = player_white
        self.__black__ = player_black
        self.__turn_white__ = True
        self.__available__ = []
        self.__rolled__ = False

    def start(self):
        self.__board__.setup_start_position()
        self.__turn_white__ = True
        self.__available__.clear()
        self.__rolled__ = False

    def current_player(self):
        return self.__white__ if self.__turn_white__ else self.__black__

    def other_player(self):
        return self.__black__ if self.__turn_white__ else self.__white__

    def get_board(self):
        return self.__board__

    def get_available_moves(self):
        return list(self.__available__)

    def roll(self):
        d1, d2 = self.__dice__.roll()
        self.__available__ = [d1, d2] if d1 != d2 else [d1] * 4
        self.__rolled__ = True
        return (d1, d2)

    def end_turn(self):
        self.__turn_white__ = not self.__turn_white__
        self.__available__.clear()
        self.__rolled__ = False

    def has_winner(self):
        if self.__board__.get_home_count("white") == 15:
            return self.__white__
        if self.__board__.get_home_count("black") == 15:
            return self.__black__
        return None

    def __color__(self):
        return "white" if self.__turn_white__ else "black"

    def __consume_exact__(self, dist):
        if dist in self.__available__:
            self.__available__.remove(dist)
            return True
        return False

    def __consume_min_ge__(self, dist):
        """Devuelve el menor valor >= dist, o False si no hay."""
        mayores = [v for v in self.__available__ if v >= dist]
        if not mayores:
            return False
        elegido = min(mayores)
        self.__available__.remove(elegido)
        return elegido

    def __distance_board__(self, color, src, dest):
        if color == "white":
            return dest - src if dest > src else -1
        return src - dest if dest < src else -1

    def __distance_bar_enter__(self, color, dest):
        if color == "white":
            return dest + 1 if 0 <= dest <= 5 else -1
        return 24 - dest if 18 <= dest <= 23 else -1

    def __distance_bear_off__(self, color, src):
        if color == "white":
            return 24 - src if 0 <= src <= 23 else -1
        return src + 1 if 0 <= src <= 23 else -1

    def __there_is_behind_in_home__(self, color, src):
        if color == "white":
            for i in range(18, src):
                if self.__board__.count_color_on_point(i, "white") > 0:
                    return True
            return False
        for i in range(src + 1, 6):
            if self.__board__.count_color_on_point(i, "black") > 0:
                return True
        return False

    def apply_move(self, src, dest):
        if not self.__rolled__ or not self.__available__:
            return False

        color = self.__color__()

        # --- Fichas en la barra ---
        if self.__board__.get_bar_count(color) > 0 and src != -1:
            return False

        # --- Movimiento desde la barra ---
        if src == -1:
            dist = self.__distance_bar_enter__(color, dest)
            if dist <= 0 or not self.__consume_exact__(dist):
                return False
            ok = self.__board__.move_from_bar(color, dest)
            if not ok:
                self.__available__.append(dist)
                return False
            return True

        # --- BEAR OFF ---
        if dest == -2:
            if not self.__board__.all_in_home(color):
                return False
            if not (0 <= src <= 23):
                return False
            if self.__board__.top_color_on_point(src) != color:
                return False

            dist = self.__distance_bear_off__(color, src)
            if dist <= 0:
                return False

            # --- Caso exacto ---
            if self.__consume_exact__(dist):
                ok = self.__board__.bear_off_from(color, src)
                if not ok:
                    self.__available__.append(dist)
                    return False
                return True

            # --- Caso dado mayor (sin fichas detrás) ---
            if not self.__there_is_behind_in_home__(color, src):
                consumido = self.__consume_min_ge__(dist)
                if consumido is not False:
                    ok = self.__board__.bear_off_from(color, src)
                    if ok:
                        return True
                    # si falla, restaurar el dado y agregar 1
                    self.__available__.append(consumido)
                    if 1 not in self.__available__:
                        self.__available__.append(1)
                    return False
            return False

        # --- Movimiento normal ---
        if not (0 <= src <= 23 and 0 <= dest <= 23):
            return False
        if self.__board__.top_color_on_point(src) != color:
            return False

        dist = self.__distance_board__(color, src, dest)
        if dist <= 0 or not self.__consume_exact__(dist):
            return False

        try:
            ok = self.__board__.move_on_board(color, src, dest)
        except Exception:
            return False

        if not ok:
            self.__available__.append(dist)
            return False
        return True
