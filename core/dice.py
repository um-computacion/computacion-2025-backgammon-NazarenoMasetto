import random

class Dice:
    """
    Dados del juego.
    """

    def __init__(self):
        self.__ultimo_resultado__ = None

    def roll(self):
        """
        Tira dos dados (1 a 6) y guarda el resultado.
        """
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self.__ultimo_resultado__ = (d1, d2)
        return (d1, d2)

    def get_last(self):
        """
        Devuelve la última tirada o None si todavía no se tiró.
        """
        return self.__ultimo_resultado__

    def is_double(self):
        """
        Devuelve True si la última tirada fue doble.
        """
        if self.__ultimo_resultado__ is None:
            return False
        return self.__ultimo_resultado__[0] == self.__ultimo_resultado__[1]
