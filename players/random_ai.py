import sys
sys.path.append("../game_components")

from player import Player
from card import CardType
from card import CardColor

import random

class RandomPlayer(Player):

    def __init__(self, name):
        self.name = name
    
    def perform_move(self, top_card):
        valid_cards = [x for x in self.hand if x == top_card]
        card = random.choice(valid_cards)
        if card.card_type == CardType.WILD:
            random_color = CardType.WILD
            while random_color != CardType.WILD:
                random_color = random.choice(list(CardColor))
            card.card_color = random_color
        return card

    def notify(self, card, player, msg=None):
        pass
    
    def request_draw(self, card, top_card):
        if card != top_card:
            return False
        else:
            return True

    def request_challenge(self, player):
        return random.randint(1, 100) % 2 == 0

    def challenged_hand(self, player, cards):
        pass

    