from card import Color
from card import Type
from card import Card
from random import shuffle

class Deck():
    def __init__(self):
        self.cards = list()

        # Add two of each colored card (one of each zero)
        first = True
        for i in range(2):
            for c in list(Color):
                for t in list(Type):
                    if t != Type.WILD and t != Type.WILD_DRAW_FOUR and c != Color.WILD:
                        if not(t == Type.ZERO and first):
                            self.cards.append(Card(c, t))
            first = False

        # Add 4 of each wild card
        for i in range(4):
            self.cards.append(Card(Color.WILD, Type.WILD))
            self.cards.append(Card(Color.WILD, Type.WILD_DRAW_FOUR))
            
        shuffle(self.cards)
        
    def draw_card(self):
        if len(self.cards) != 0:
            return self.cards.pop()