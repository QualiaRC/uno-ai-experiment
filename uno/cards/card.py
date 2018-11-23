from enum import Enum

class Card():
    def __init__(self, color, card_type):
        self.color = color
        self.card_type = card_type

    def print_card(self):
        print(f'{self.color}\t{self.card_type}')

    def matches_card(self, card):
        return self.color == card.color or \
               self.card_type == card.card_type or \
               self.color == Color.WILD or card.color == Color.WILD

class Color(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    WILD = 5

    def __eq__(self, b):
        return self.value == b.value

    def __ne__(self, b):
        return self.value != b.value

class Type(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    DRAW_TWO = 10
    SKIP = 11
    REVERSE = 12
    WILD = 13
    WILD_DRAW_FOUR = 14

    def __eq__(self, b):
        return self.value == b.value
    
    def __ne__(self, b):
        return self.value != b.value