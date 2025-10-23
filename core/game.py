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
        self.__available__ = []
        self.__rolled__ = False

    def current_player(self):
        if self.__turn_white__:
            return self.__white__
        return self.__black__

    def other_player(self):
        if self.__turn_white__:
            return self.__black__
        return self.__white__

    def get_board(self):
        return self.__board__

    def get_available_moves(self):
        copia = []
        i = 0
        while i < len(self.__available__):
            copia.append(self.__available__[i])
            i = i + 1
        return copia

    def roll(self):
        r = self.__dice__.roll()
        self.__available__ = []
        d1 = r[0]
        d2 = r[1]
        if d1 == d2:
            self.__available__.append(d1)
            self.__available__.append(d1)
            self.__available__.append(d1)
            self.__available__.append(d1)
        else:
            self.__available__.append(d1)
            self.__available__.append(d2)
        self.__rolled__ = True
        return r

    def end_turn(self):
        self.__turn_white__ = not self.__turn_white__
        self.__available__ = []
        self.__rolled__ = False

    def has_winner(self):
        if self.__board__.get_home_count("white") == 15:
            return self.__white__
        if self.__board__.get_home_count("black") == 15:
            return self.__black__
        return None

    def __color__(self):
        if self.__turn_white__:
            return "white"
        return "black"

    def __consume_exact__(self, dist):
        i = 0
        while i < len(self.__available__):
            if self.__available__[i] == dist:
                self.__available__.pop(i)
                return True
            i = i + 1
        return False

    def __consume_min_ge__(self, dist):
        pos = -1
        best = None
        i = 0
        while i < len(self.__available__):
            v = self.__available__[i]
            if v >= dist:
                if best is None or v < best:
                    best = v
                    pos = i
            i = i + 1
        if pos != -1:
            self.__available__.pop(pos)
            return True
        return False

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
            if dest < 0 or dest > 5:
                return -1
            return dest + 1
        else:
            if dest < 18 or dest > 23:
                return -1
            return 24 - dest

    def __distance_bear_off__(self, color, src):
        if color == "white":
            return 24 - src
        else:
            return src + 1

    def __there_is_behind_in_home__(self, color, src):
        if color == "white":
            i = 18
            while i < src:
                if self.__board__.count_color_on_point(i, "white") > 0:
                    return True
                i = i + 1
            return False
        else:
            i = 5
            while i > src:
                if self.__board__.count_color_on_point(i, "black") > 0:
                    return True
                i = i - 1
            return False

    def apply_move(self, src, dest):
        if not self.__rolled__:
            return False
        if len(self.__available__) == 0:
            return False

        color = self.__color__()

        if self.__board__.get_bar_count(color) > 0:
            if src != -1:
                return False

        if src == -1:
            dist = self.__distance_bar_enter__(color, dest)
            if dist <= 0:
                return False
            if not self.__consume_exact__(dist):
                return False
            ok = self.__board__.move_from_bar(color, dest)
            if not ok:
                self.__available__.append(dist)
                return False
            return True

        if dest == -2:
            if not self.__board__.all_in_home(color):
                return False
            if src < 0 or src > 23:
                return False
            top = self.__board__.top_color_on_point(src)
            if top != color:
                return False

            dist = self.__distance_bear_off__(color, src)
            if self.__consume_exact__(dist):
                ok = self.__board__.bear_off_from(color, src)
                if not ok:
                    self.__available__.append(dist)
                    return False
                return True

            if self.__there_is_behind_in_home__(color, src):
                return False

            if self.__consume_min_ge__(dist):
                ok = self.__board__.bear_off_from(color, src)
                if not ok:
                    self.__available__.append(1)
                    return False
                return True

            return False

        if src < 0 or src > 23:
            return False
        if dest < 0 or dest > 23:
            return False
        if self.__board__.top_color_on_point(src) != color:
            return False

        dist = self.__distance_board__(color, src, dest)
        if dist <= 0:
            return False

        if not self.__consume_exact__(dist):
            return False

        ok = self.__board__.move_on_board(color, src, dest)
        if not ok:
            self.__available__.append(dist)
            return False
        return True
