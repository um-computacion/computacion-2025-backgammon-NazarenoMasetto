from .checker import Checker

class Board:
   
    def _init_(self):
        self._puntos_ = []
        i = 0
        while i < 24:
            self._puntos_.append([])
            i = i + 1
        self._bar_white_ = []
        self._bar_black_ = []
        self._home_white_ = []
        self._home_black_ = []

    def get_point(self, i):
        if i < 0 or i > 23:
            return None
        return self._puntos_[i]

    def clear(self):
        i = 0
        while i < 24:
            self._puntos_[i] = []
            i = i + 1
        self._bar_white_ = []
        self._bar_black_ = []
        self._home_white_ = []
        self._home_black_ = []

    def setup_start_position(self):
        
        self.clear()

        k = 0
        while k < 2:
            self._puntos_[0].append(Checker("white"))
            self._puntos_[23].append(Checker("black"))
            k = k + 1

        k = 0
        while k < 5:
            self._puntos_[11].append(Checker("white"))
            self._puntos_[12].append(Checker("black"))
            k = k + 1

        k = 0
        while k < 3:
            self._puntos_[16].append(Checker("white"))
            self._puntos_[7].append(Checker("black"))
            k = k + 1

        k = 0
        while k < 5:
            self._puntos_[18].append(Checker("white"))
            self._puntos_[5].append(Checker("black"))
            k = k + 1

    def add_checker_to_point(self, i, color):
        if i < 0 or i > 23:
            return False
        ficha = Checker(color)
        self._puntos_[i].append(ficha)
        return True

    def pop_checker_from_point(self, i):
        if i < 0 or i > 23:
            return None
        if len(self._puntos_[i]) == 0:
            return None
        return self._puntos_[i].pop()

    def top_color_on_point(self, i):
        if i < 0 or i > 23:
            return None
        if len(self._puntos_[i]) == 0:
            return None
        return self._puntos_[i][-1].get_color()

    def count_color_on_point(self, i, color):
        if i < 0 or i > 23:
            return 0
        total = 0
        j = 0
        while j < len(self._puntos_[i]):
            ficha = self._puntos_[i][j]
            if ficha.get_color() == color:
                total = total + 1
            j = j + 1
        return total

    def get_bar_count(self, color):
        if color == "white":
            return len(self._bar_white_)
        return len(self._bar_black_)

    def get_home_count(self, color):
        if color == "white":
            return len(self._home_white_)
        return len(self._home_black_)

    def add_to_bar(self, color):
        ficha = Checker(color)
        if color == "white":
            self._bar_white_.append(ficha)
        else:
            self._bar_black_.append(ficha)

    def remove_from_bar(self, color):
        if color == "white":
            if len(self._bar_white_) > 0:
                return self._bar_white_.pop()
            return None
        else:
            if len(self._bar_black_) > 0:
                return self._bar_black_.pop()
            return None

    def all_in_home(self, color):
     
        total_en_tablero = 0
        i = 0
        while i < 24:
            total_en_tablero = total_en_tablero + self.count_color_on_point(i, color)
            i = i + 1
        total_fuera = self.get_home_count(color)
        total_en_barra = self.get_bar_count(color)
        total = total_en_tablero + total_fuera + total_en_barra
        # 15 fichas por color
        if total != 15:
            
            pass

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
        if len(self._puntos_[dest]) == 0:
            return True
        top = self._puntos_[dest][-1].get_color()
        if top == color:
            return True
        
        cant = len(self._puntos_[dest])
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
        
            if len(self._puntos[dest]) == 1 and self.puntos_[dest][-1].get_color() == "black":
                capturada = self._puntos_[dest].pop()
                self._bar_black_.append(capturada)
            self._puntos_[dest].append(ficha)
            return True
        else:
            
            if dest < 18 or dest > 23:
                return False
            if not self.can_land(dest, "black"):
                return False
            ficha = self.remove_from_bar("black")
            if ficha is None:
                return False
            if len(self._puntos[dest]) == 1 and self.puntos_[dest][-1].get_color() == "white":
                capturada = self._puntos_[dest].pop()
                self._bar_white_.append(capturada)
            self._puntos_[dest].append(ficha)
            return True

    def move_on_board(self, color, src, dest):
        
        if src < 0 or src > 23:
            return False
        if dest < 0 or dest > 23:
            return False
        if len(self._puntos_[src]) == 0:
            return False
        if self._puntos_[src][-1].get_color() != color:
            return False
        if not self.can_land(dest, color):
            return False

        ficha = self._puntos_[src].pop()

        if len(self._puntos_[dest]) == 1:
            otro = self._puntos_[dest][-1]
            if otro.get_color() != color:
                self._puntos_[dest].pop()
                if color == "white":
                    self._bar_black_.append(otro)
                else:
                    self._bar_white_.append(otro)

        self._puntos_[dest].append(ficha)
        return True

    def bear_off_from(self, color, src):
        
        if src < 0 or src > 23:
            return False
        if len(self._puntos_[src]) == 0:
            return False
        if self._puntos_[src][-1].get_color() != color:
            return False
        ficha = self._puntos_[src].pop()
        if color == "white":
            self._home_white_.append(ficha)
        else:
            self._home_black_.append(ficha)
        return True