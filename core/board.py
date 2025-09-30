from .checker import Checker

class Board:
    """
    Tablero de Backgammon con 24 puntos, barra y home.
    """

    def __init__(self):
        self.__puntos__ = []
        i = 0
        while i < 24:
            self.__puntos__.append([])
            i = i + 1
        self.__bar_white__ = []
        self.__bar_black__ = []
        self.__home_white__ = []
        self.__home_black__ = []

    def get_point(self, i):
        if i < 0 or i > 23:
            return None
        return self.__puntos__[i]

    def clear(self):
        i = 0
        while i < 24:
            self.__puntos__[i] = []
            i = i + 1
        self.__bar_white__ = []
        self.__bar_black__ = []
        self.__home_white__ = []
        self.__home_black__ = []

    def setup_start_position(self):
        self.clear()

        k = 0
        while k < 2:
            self.__puntos__[0].append(Checker("white"))
            self.__puntos__[23].append(Checker("black"))
            k = k + 1

        k = 0
        while k < 5:
            self.__puntos__[11].append(Checker("white"))
            self.__puntos__[12].append(Checker("black"))
            k = k + 1

        k = 0
        while k < 3:
            self.__puntos__[16].append(Checker("white"))
            self.__puntos__[7].append(Checker("black"))
            k = k + 1

        k = 0
        while k < 5:
            self.__puntos__[18].append(Checker("white"))
            self.__puntos__[5].append(Checker("black"))
            k = k + 1

    def add_checker_to_point(self, i, color):
        if i < 0 or i > 23:
            return False
        ficha = Checker(color)
        self.__puntos__[i].append(ficha)
        return True

    def pop_checker_from_point(self, i):
        if i < 0 or i > 23:
            return None
        if len(self.__puntos__[i]) == 0:
            return None
        return self.__puntos__[i].pop()