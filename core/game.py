from .board import Board
from .dice import Dice
from .player import Player

class BackgammonGame:


    def __init__(self, player_white, player_black):
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__players__ = (player_white, player_black)
        self.__turn_index__ = 0
        self.__available_moves__ = []
        self.__last_roll__ = None

    def start(self):
        
        self.__board__.setup_start_position()

    def current_player(self):
        
        return self.__players__[self.__turn_index__]

    def other_player(self):
      
        if self.__turn_index__ == 0:
            return self.__players__[1]
        return self.__players__[0]

    def roll(self):
       
        resultado = self.__dice__.roll()
        self.__last_roll__ = resultado
        self.__available_moves__ = []
        d1 = resultado[0]
        d2 = resultado[1]
        if d1 == d2:
            i = 0
            while i < 4:
                self.__available_moves__.append(d1)
                i = i + 1
        else:
            self.__available_moves__.append(d1)
            self.__available_moves__.append(d2)
        return resultado