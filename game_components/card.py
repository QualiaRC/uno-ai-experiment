from enum import Enum


# Listing all possible colors for cards.
class CardColor(Enum):
    RED = 1
    BLUE = 2
    YELLOW = 3
    GREEN = 4
    WILD = 5

    def __str__(self):
        return self.name


# Listing all possible types of cards.
class CardType(Enum):
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
    REVERSE = 10
    SKIP = 11
    DRAW_TWO = 12
    DRAW_FOUR = 13
    WILD = 14

    def __str__(self):
        return self.name


# Class representing a playing card in UNO.
class Card:

    # Takes in the CardColor and CardType of the card.
    def __init__(self, card_color, card_type):
        self.card_color = card_color
        self.card_type = card_type
    
    # Returns True if the card's type is non-numerical.
    @property
    def special(self):
        special_cards = [CardType.REVERSE, CardType.SKIP, CardType.DRAW_TWO, CardType.DRAW_FOUR, CardType.WILD]
        return self.card_type in special_cards

    # Cards are considered equal if their color or type matches.
    # In this case, DRAW_FOUR and WILD are the same card.
    def __eq__(self, other):

        # Splitting up the conditionals for readability.
        # Checking for regular equalities.
        color_match = self.card_color == other.card_color
        type_match = self.card_type == other.card_type
        wild_match = self.card_color == CardColor.WILD or other.card_color == CardColor.WILD

        return color_match or type_match or wild_match

    def __str__(self):
        if (self.card_color == CardType.WILD or self.card_color == CardType.DRAW_FOUR):
            return f"[ {self.card_type} ]"
        else:
            return f"[ {self.card_color} {self.card_type} ]"

    