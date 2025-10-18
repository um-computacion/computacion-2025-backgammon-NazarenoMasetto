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