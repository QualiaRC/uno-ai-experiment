from uno.players.player import Player
from uno.players.minimax_algorithm.minimax_algo import Minimax
from uno.game_components.card import *
from uno.game_components.deck import Deck

from copy import deepcopy
import random

class MinimaxPlayer(Player):

    def __init__(self, name, players, functions):
        super().__init__(name)
        self.name = name
        self.algo = Minimax(self.name, players, functions)
        self.current_deck_total = 100
        self.current_player_order = None
        self.previous_player = None
    
    # Select a card by generating a decision tree, and selecting a card based on heuristic functions etc.
    def perform_move(self, top_card):
        chosen_card =  self.algo.get_card(deepcopy(self.hand), deepcopy(top_card), self.current_deck_total, self.current_player_order, self.previous_player)
        #print(f"chosen_card: {chosen_card} against top card: {top_card}")
        #print("out of..")
        #[print(f"  {x}") for x in self.hand]
        if chosen_card is None:
            return None
        for i in range(len(self.hand)):
            if ((chosen_card.card_type == CardType.WILD and self.hand[i].card_type == CardType.WILD)
                or (chosen_card.card_type == CardType.DRAW_FOUR and self.hand[i].card_type == CardType.DRAW_FOUR)):
                self.hand[i].card_color = chosen_card.card_color
                selected_card = self.hand.pop(i)
                return selected_card
            elif self.hand[i] == chosen_card:
                selected_card = self.hand.pop(i)
                return selected_card

    # Handle the card given by adding it to relevant structures keeping track of cards played.
    def notify(self, card, top_card, player, deck_total, msg=None):

        if deck_total > self.current_deck_total:
            self.algo.cards_played = [deepcopy(top_card)]

        if card:
            self.algo.cards_played += [deepcopy(card)]
            self.previous_player = player.name
            if card in self.algo.mystery_hands[player.name]:
                self.algo.mystery_hands[player.name].remove(card)
            elif None in self.algo.mystery_hands[player.name]:
                self.algo.mystery_hands[player.name].remove(None)
        self.current_deck_total = deck_total
    
    # Make a decision about whether to play a drawn card or not.
    def request_draw(self, card, top_card):
        if not card.same(top_card):
            return False
        else:
            if card.card_type == CardType.WILD or card.card_type == CardType.DRAW_FOUR:
                self.select_wild_color(card)

            return True

    # Make a decision about whether to challenge a Draw Four, based on the odds of the player bluffing.
    def request_challenge(self, player, top_card):
        # Get the cards that have been played so far.
        cards_played = self.algo.cards_played
        
        # Check if we know anything about the player's hand, and challenge them if they potentially have a card they shouldn't have.
        for card in self.algo.mystery_hands[player.name]:
            if not (card is None) and card.same(top_card) and card.card_type != CardType.DRAW_FOUR:
                return True
        
        # Calculate the odds of the player having a card matching the top card.
        all_matches = 0
        all_cards = Deck()
        for card in all_cards:
            if card.same(top_card):
                all_matches += 1
        
        # Count the number of cards that can be matches that have already been played.
        matches_depleted = 0
        for card in cards_played:
            if card.card_type == CardType.WILD or card.card_type == CardType.DRAW_FOUR:
                matches_depleted += 1
            elif card.same(top_card):
                matches_depleted += 1

        # Make a chance table that represents the probability that the challenger has another playable card, and return it.

        table = [False for _ in range(matches_depleted)] + [True for _ in range(all_matches - matches_depleted)]
        return random.choice(table)

    # Handle the cards given by adding it to relevant structures keeping track of cards.
    def challenged_hand(self, player, cards):
        self.algo.mystery_hands[player.name] = deepcopy(cards)

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