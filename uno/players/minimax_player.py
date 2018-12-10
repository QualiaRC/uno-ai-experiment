from uno.players.player import Player
from uno.players.minimax_algorithm.minimax_algo import Minimax
from uno.game_components.card import *

from copy import deepcopy
import random

class MinimaxPlayer(Player):

    def __init__(self, name, players):
        super().__init__(name)
        self.name = name
        self.algo = Minimax(self.name, players)
        self.current_deck_total = 100
        self.current_player_order = None
        self.previous_player = None
    
    # Select a card by generating a decision tree, and selecting a card based on heuristic functions etc.
    def perform_move(self, top_card):
        chosen_card =  self.algo.get_card(deepcopy(self.hand), deepcopy(top_card), self.current_deck_total, self.current_player_order, self.previous_player)
        #print(f"chosen_card: {chosen_card}")
        #print("out of..")
        #[print(f"  {x}") for x in self.hand]
        if chosen_card is None:
            return None
        for i in range(len(self.hand)):
            if self.hand[i].card_type == chosen_card.card_type and self.hand[i].card_color == chosen_card.card_color:
                selected_card = self.hand.pop(i)
                if selected_card.card_type == CardType.WILD or selected_card.card_type == CardType.DRAW_FOUR:
                    self.select_wild_color(selected_card)
                return selected_card
    # Handle the card given by adding it to relevant structures keeping track of cards played.
    def notify(self, card, top_card, player, deck_total, msg=None):
        if card:
            self.algo.cards_played += [deepcopy(card)]
            self.previous_player = player.name
        self.current_deck_total = deck_total
    
    # Make a decision about whether to play a drawn card or not.
    def request_draw(self, card, top_card):
        if card != top_card:
            return False
        else:
            if card.card_type == CardType.WILD or card.card_type == CardType.DRAW_FOUR:
                self.select_wild_color(card)

            return True

    # Make a decision about whether to challenge a Draw Four, based on the odds of the player bluffing.
    def request_challenge(self, player):
        return (random.randint(1,2) == 1)

    # Handle the cards given by adding it to relevant structures keeping track of cards.
    def challenged_hand(self, player, cards):
        pass

    # Don't actually care about sent messages, do nothing.
    def send_msg(self, msg):
        pass

    def send_player_order(self, player_list):
        self.current_player_order = player_list

    # Select an appropriate card color.
    def select_wild_color(self, wild_card):
        color_count = {
                    CardColor.BLUE: 0,
                    CardColor.RED: 0,
                    CardColor.GREEN: 0,
                    CardColor.YELLOW: 0,
        }
        for card in self.hand:
            if not card.card_color == CardColor.WILD:
                color_count[card.card_color] += 1
        
        wild_card.card_color = max(color_count, key=color_count.get)