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

    