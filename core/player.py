class Player:
    def __init__(self, nombre, color):
        self.__nombre__ = nombre
        self.__color__ = color
        self.__fichas_en_barra__ = 0
        self.__fichas_fuera__ = 0

    def get_name(self):
        return self.__nombre__

    def get_color(self):
        return self.__color__