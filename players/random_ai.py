from players.player import Player
from game_components.card import CardType
from game_components.card import CardColor

import random

class RandomPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.name = name
    
    # Select a random card, and play it, with no strategy involved.
    def perform_move(self, top_card):

        # Get a random valid card from the hand.
        valid_cards = [x for x in self.hand if x == top_card]
        if valid_cards == []:  # Return None if no cards can be played.
            return None
        card = random.choice(valid_cards)

        # Handle WILD and DRAW FOUR cards.
        if card.card_type == CardType.WILD or card.card_type == CardType.DRAW_FOUR:
            random_color = CardType.WILD
            while random_color == CardType.WILD:
                random_color = random.choice(list(CardColor))
            card.card_color = random_color

        # Remove the card, and return it.
        self.hand.remove(card)
        return card

    # Do nothing on other turns, since the AI is keeping track of nothing.
    def notify(self, card, top_card, player, msg=None):
        pass
    
    # Always play the card drawn if the AI can play it.
    def request_draw(self, card, top_card):
        if card != top_card:
            return False
        else:
            if card.card_type == CardType.WILD or card.card_type == CardType.DRAW_FOUR:
                random_color = CardType.WILD
                while random_color == CardType.WILD:
                    random_color = random.choice(list(CardColor))
                card.card_color = random_color
            return True

    # 50/50 chance for challenging a DRAW FOUR card.
    def request_challenge(self, player):
        return random.randint(1, 100) % 2 == 0

    # Don't actually care about the shown hand, do nothing.
    def challenged_hand(self, player, cards):
        pass

    # Don't actually care about sent messages, do nothing.
    def send_msg(self, msg):
        pass

    