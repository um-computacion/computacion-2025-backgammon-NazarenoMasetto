import random

class Dice:
    def roll(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return (d1, d2)
