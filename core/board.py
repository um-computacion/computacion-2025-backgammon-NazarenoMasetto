from .checker import Checker

class Board:
    

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

    def add_checker_to_point(self, i, color):
        
        if i < 0 or i > 23:
            return False
        ficha = Checker(color)
        self.__puntos__[i].append(ficha)
        return True

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
