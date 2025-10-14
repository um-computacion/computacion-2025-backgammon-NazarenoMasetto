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

    def get_bar_count(self):
        return self.__fichas_en_barra__

    def get_off_count(self):
        return self.__fichas_fuera__

    def add_to_bar(self, cantidad):
        if cantidad < 0:
            return
        self.__fichas_en_barra__ = self.__fichas_en_barra__ + cantidad

    def remove_from_bar(self, cantidad):
        if cantidad < 0:
            return
        nuevo = self.__fichas_en_barra__ - cantidad
        if nuevo < 0:
            nuevo = 0
        self.__fichas_en_barra__ = nuevo

    def add_off(self, cantidad):
        if cantidad < 0:
            return
        self.__fichas_fuera__ = self.__fichas_fuera__ + cantidad
