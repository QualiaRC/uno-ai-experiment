from random import shuffle
from copy import deepcopy
from uno.game_components.card import *
from uno.game_components.discard_pile import DiscardPile

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
        # Get the top card of the pile out
        top_card = cards.top
        cards.remove(top_card)
        # Change all WILD cards in the deck to be colored.
        for card in cards:
            if card.card_type == CardType.DRAW_FOUR or card.card_type == CardType.WILD:
                card.card_color = CardColor.WILD
        # Shuffle the cards, and place them back in the deck.
        self + shuffle(cards)
        cards = [top_card]

    # Draw a given amount of cards from the deck.
    # Returns a list of the cards drawn.
    def draw(self, amt=1):
        return [self.pop() for _ in range(amt)]