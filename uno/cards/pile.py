from card import Color
from card import Type
from card import Card
from random import shuffle

class Pile():
    def __init__(self):
        self.cards = list()

    def place_card(self, card):
        self.cards.append(card)

    def get_top_card(self):
        return self.cards[-1]