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
