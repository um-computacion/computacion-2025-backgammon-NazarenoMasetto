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

    def top_color_on_point(self, i):
        if i < 0 or i > 23:
            return None
        if len(self.__puntos__[i]) == 0:
            return None
        return self.__puntos__[i][-1].get_color()

    def count_color_on_point(self, i, color):
        if i < 0 or i > 23:
            return 0
        total = 0
        j = 0
        while j < len(self.__puntos__[i]):
            ficha = self.__puntos__[i][j]
            if ficha.get_color() == color:
                total = total + 1
            j = j + 1
        return total

    def get_bar_count(self, color):
        if color == "white":
            return len(self.__bar_white__)
        return len(self.__bar_black__)

    def get_home_count(self, color):
        if color == "white":
            return len(self.__home_white__)
        return len(self.__home_black__)

    def add_to_bar(self, color):
        ficha = Checker(color)
        if color == "white":
            self.__bar_white__.append(ficha)
        else:
            self.__bar_black__.append(ficha)

    def remove_from_bar(self, color):
        if color == "white":
            if len(self.__bar_white__) > 0:
                return self.__bar_white__.pop()
            return None
        else:
            if len(self.__bar_black__) > 0:
                return self.__bar_black__.pop()
            return None

    def all_in_home(self, color):
        if color == "white":
            i = 0
            while i < 18:
                if self.count_color_on_point(i, "white") > 0:
                    return False
                i = i + 1
            if self.get_bar_count("white") > 0:
                return False
            return True
        else:
            i = 6
            while i < 24:
                if self.count_color_on_point(i, "black") > 0:
                    return False
                i = i + 1
            if self.get_bar_count("black") > 0:
                return False
            return True

    def can_land(self, dest, color):
        if dest < 0 or dest > 23:
            return False
        if len(self.__puntos__[dest]) == 0:
            return True
        top = self.__puntos__[dest][-1].get_color()
        if top == color:
            return True
        cant = len(self.__puntos__[dest])
        if cant == 1:
            return True
        return False

    def move_from_bar(self, color, dest):
        if color == "white":
            if dest < 0 or dest > 5:
                return False
            if not self.can_land(dest, "white"):
                return False
            ficha = self.remove_from_bar("white")
            if ficha is None:
                return False
            if len(self.__puntos__[dest]) == 1 and self.__puntos__[dest][-1].get_color() == "black":
                capturada = self.__puntos__[dest].pop()
                self.__bar_black__.append(capturada)
            self.__puntos__[dest].append(ficha)
            return True
        else:
            if dest < 18 or dest > 23:
                return False
            if not self.can_land(dest, "black"):
                return False
            ficha = self.remove_from_bar("black")
            if ficha is None:
                return False
            if len(self.__puntos__[dest]) == 1 and self.__puntos__[dest][-1].get_color() == "white":
                capturada = self.__puntos__[dest].pop()
                self.__bar_white__.append(capturada)
            self.__puntos__[dest].append(ficha)
            return True

    def move_on_board(self, color, src, dest):
        if src < 0 or src > 23:
            return False
        if dest < 0 or dest > 23:
            return False
        if len(self.__puntos__[src]) == 0:
            return False
        if self.__puntos__[src][-1].get_color() != color:
            return False
        if not self.can_land(dest, color):
            return False

        ficha = self.__puntos__[src].pop()

        if len(self.__puntos__[dest]) == 1:
            otro = self.__puntos__[dest][-1]
            if otro.get_color() != color:
                self.__puntos__[dest].pop()
                if color == "white":
                    self.__bar_black__.append(otro)
                else:
                    self.__bar_white__.append(otro)

        self.__puntos__[dest].append(ficha)
        return True

    def bear_off_from(self, color, src):
        if src < 0 or src > 23:
            return False
        if len(self.__puntos__[src]) == 0:
            return False
        if self.__puntos__[src][-1].get_color() != color:
            return False
        ficha = self.__puntos__[src].pop()
        if color == "white":
            self.__home_white__.append(ficha)
        else:
            self.__home_black__.append(ficha)
        return True
