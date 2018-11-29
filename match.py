import sys
sys.path.append("./game_components")

from deck import Deck
from discard_pile import DiscardPile
from card import *
from player import Player

from random import shuffle

class Match:

    def __init__(self, players):
        
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        
        # Shuffle the players to ensure fairness in the player order.
        self.players = players
        shuffle(self.players)

        # Deal the cards to the players.
        self.deal_cards()

        # Add a card to the discard pile.
        self.discard_pile.add_card(self.deck.draw())

        # in_progress signifies that the game in progress.
        self.in_progress = True

        # Start the game loop.
        self.game_loop()

        # Dictionary of methods to speed up processing.
        self.special_methods = {
            CardType.SKIP: self.skip,
            CardType.REVERSE: self.reverse
        }

    # Deal cards deals 7 cards to each player from the deck.
    def deal_cards(self):
        for _ in range(7):
            for player in self.players:
                player.give_card(self.deck.draw())

    # Calls notify on each player on the queue.
    def notify_all_players(self, card, player):
        pass
    
    def game_loop(self):

        print(f"Player order: {[x for x in self.players]}\n")

        while self.in_progress:

            current_player = self.players.popleft()
            played_card = current_player.perform_move(self.discard_pile.top)
            self.handle_card(played_card, current_player)
            if current_player.cards_left == 0:
                # notify winner
                self.in_progress = False
                print(f"Player {current_player} has won!\n<Press ENTER to close>)")


    def handle_card(self, card, player):
        
        if card.special:
            self.special_methods[card.card_type](card, player)
        else:
            # handle normal card

        self.discard_pile.add_card(card)


    def skip(self, card, player):
        skipped_player = self.players.popleft()
        self.notify_all_players(card, player)
        self.players.append(player)
        self.players.append(skipped_player)

    def reverse(self, card, player):
        pass

    def draw_two(self, card, player):
        pass

    def draw_four(self, card, player):
        pass

    def wild(self, card, player):
        pass