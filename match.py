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
            CardType.REVERSE: self.reverse,
            CardType.DRAW_TWO: self.draw_two,
            CardType.DRAW_FOUR: self.draw_four
        }

    # Deal cards deals 7 cards to each player from the deck.
    def deal_cards(self):
        for _ in range(7):
            for player in self.players:
                player.give_card(self.deck.draw())

    # Calls notify on each player on the queue.
    def notify_all_players(self, card, player, msg=None):
        for p in self.players:
            p.notify(card, player, msg)
    
    # The main loop of the game.
    # This loop continues until a player wins, or until an error occurs.
    def game_loop(self):

        player_string = [(f"\t{x}\n") for x in self.players]
        print(f"Player order:\n {x for x in player_string}\n")

        while self.in_progress:

            # Get the next player in the queue, and ask them to play a card.
            current_player = self.players.popleft()
            played_card = current_player.perform_move(self.discard_pile.top)

            # Handle the card played by the player.
            self.handle_card(played_card, current_player)

            # Check if the current player has won.
            # If so, notify the winner, and end the game loop.
            if current_player.cards_left == 0:
                self.in_progress = False
                print(f"Player {current_player} has won!\n<Press ENTER to close>)")

    # Play the given card.
    # This will perform special moves if the given card warrants them.
    # Throws an exception if the given card is invalid.
    def handle_card(self, card, player):
        
        # If the card is None, do draw card logic
        if card is None:
            drawn_card = self.deck.draw(1)
            if player.request_draw(drawn_card[0]):
                card = drawn_card[0]
            else:
                self.notify_all_players(None, player)
                player.add_card(drawn_card)
                return

        # If the card is special, run it's specific function.
        # These functions are responsible for putting the player back on the queue.
        if card.special:
            self.special_methods[card.card_type](card, player)
        
        # If the card isn't special, play it normally.
        else:    
            self.notify_all_players(card, player)
            self.players.append(player)

        # Check if the card is valid, and play if it is.
        if card != self.discard_pile.top:
            raise ValueError("Player played card that does not match the top card!")
        self.discard_pile.add_card(card)

    # Skips the next player in the queue.
    def skip(self, card, player):
        skipped_player = self.players.popleft()
        self.notify_all_players(card, player, msg=f"Player {skipped_player} has been skipped.")
        skipped_player.notify(card, player, msg=f"You have been skipped.")
        self.players.append(player)
        self.players.append(skipped_player)

    # Reverses the order of the game.
    # The message includes the new turn order of the game.
    def reverse(self, card, player):
        self.players.reverse()
        player_string = [(f"\t{x}\n") for x in self.players]
        msg = (f"The turn order has been reversed!\n"
               f"Player order:\n {[x for x in player_string]}\n")
        self.notify_all_players(card, player, msg=msg)

    # Gives two cards to the next player in the queue.
    # Also skips that player, as per the rules.
    def draw_two(self, card, player):
        drawing_player = self.players.popleft()
        self.notify_all_players(card, player, msg=f"{drawing_player} has drawn two cards, and has been skipped.")
        drawing_player.notify(card, player, msg="You have drawn two cards, and have been skipped.")
        drawing_player.give_card(self.deck.draw(2))        
        self.players.append(player)
        self.players.append(drawing_player)

    def draw_four(self, card, player):
        drawing_player = self.players.popleft()
        
        # Ask if the drawing player wants to challenge the Draw Four card.
        is_challenging = drawing_player.request_challenge()

        if is_challenging:
            
            # Show the player the opponent's hand.
            drawing_player.challenged_hand(player, player.hand)
            
            # Check if the challenge is successful.
            challenge_success = False
            for card in player.hand:
                if card == self.discard_pile.top:
                    challenge_success = True
                    break
            
            # If the challenge is successful, give the current player 6 cards,
            #  and put the drawing player back on the queue.
            if challenge_success:
                
                # Tell all non-involved players about the challenge results.
                msg = (f"Player {drawing_player}  has challenged Player {player}'s Draw Four, and succeeded!\n"
                       f"Player {player} has drawn four cards.")
                # Tell the drawing player about the challenge results.
                self.notify_all_players(card, player, msg=msg)
                drawing_player.notify(card, player, msg=f"Your challenge against {player} was successful!")
                # Give the player four cards.
                player.give_card(self.deck.draw(4))
                # Add the players back onto the queue.
                self.players.insert(0, drawing_player)
                self.players.append(player)

            else:
                # Tell all non-involved players about the challenge results.
                msg = (f"Player {drawing_player}  has challenged Player {player}'s Draw Four, and failed.\n"
                       f"Player {drawing_player} has drawn six cards, and has been skipped.")
                # Tell the drawing player about the challenge results.
                self.notify_all_players(card, player, msg=msg)
                drawing_player.notify(card, player, msg=f"Your challenge against {player} was a failure.\nYou have drawn six cards, and have been skipped.")
                # Give the drawing player six cards.
                drawing_player.give_card(self.deck.draw(6))   
                # Add the players back onto the queue.
                self.players.insert(0, drawing_player)
                self.players.append(player)

        else:
            self.notify_all_players(card, player, msg=f"{drawing_player} has drawn four cards, and has been skipped.")
            drawing_player.notify(card, player, msg="You have drawn four cards, and have been skipped.")
            drawing_player.give_card(self.deck.draw(4))        
            self.players.append(player)
            self.players.append(drawing_player)
        
