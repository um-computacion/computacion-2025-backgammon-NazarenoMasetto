import random

class Dice:
    def __init__(self):
        self.__ultimo_resultado__ = None

    def roll(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self.__ultimo_resultado__ = (d1, d2)
        return (d1, d2)

    def get_last(self):
        return self.__ultimo_resultado__

    def is_double(self):
        if self.__ultimo_resultado__ is None:
            return False
        return self.__ultimo_resultado__[0] == self.__ultimo_resultado__[1]
