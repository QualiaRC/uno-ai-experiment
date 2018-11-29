from random import shuffle
from copy import deepcopy
from card import Card
from card import CardColor
from card import CardType
from discard import DiscardPile

class Deck(list):

    # On initialization, create the deck of cards.
    # The deck represents a standard UNO deck before any cards are dealt.
    def __init__(self):
        for _ in range(4):
            self.append(Card(CardColor.WILD, CardType.WILD))
            self.append(Card(CardColor.WILD, CardType.DRAW_FOUR))

        for color in CardColor:
            if not color is CardColor.WILD:
                self.append(Card(color, CardType.ZERO))
        
        for color in CardColor:
            if not color is CardColor.WILD:
                for t in CardType:
                    if t != CardType.ZERO and t != CardType.WILD and t != CardType.DRAW_FOUR:
                        self.append(Card(color, t))
                        self.append(Card(color, t))

        shuffle(self)

    # Takes a discard pile as an argument,
    #  shuffles the cards in the discard pile,
    #  and adds it back to the deck.
    # The discard pile is emptied when this is called.
    def recycle_from_pile(self, cards : DiscardPile):
        self + shuffle(deepcopy(cards))
        cards = []

    def draw(self):
        return self.pop()