from uno.game_components.deck import Deck
from uno.game_components.discard_pile import DiscardPile
from uno.game_components.card import *
from uno.players.player import Player

from random import shuffle

class Match:

    def __init__(self, players, verbose=True):
        
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.verbose = verbose
        
        # Dictionary of methods to speed up processing.
        self.special_methods = {
            CardType.SKIP: self.skip,
            CardType.REVERSE: self.reverse,
            CardType.DRAW_TWO: self.draw_two,
            CardType.DRAW_FOUR: self.draw_four,
            CardType.WILD: self.wild
        }
        
        # Shuffle the players to ensure fairness in the player order.
        self.players = players
        shuffle(self.players)

        # Deal the cards to the players.
        self.deal_cards()

        # Add a card to the discard pile.
        self.discard_pile.add_card(self.deck.draw()[0])

        # in_progress signifies that the game in progress.
        self.in_progress = True

        # Start the game loop.
        self.winner = self.game_loop()

    # Get the current order of players by name.
    @property
    def player_list(self):
        return [x.name for x in self.players]

    # Deal cards deals 7 cards to each player from the deck.
    def deal_cards(self):
        for _ in range(7):
            for player in self.players:
                player.give_card(self.deck.draw())

    # Calls notify on each player on the queue.
    def notify_all_players(self, card, top_card, player, msg=None):
        for p in self.players:
            p.notify(card, top_card, player, len(self.deck), msg)

    # Sends all players on the queue the current order of players.
    def send_all_player_lists(self):
        for p in self.players:
            p.send_player_order(self.player_list)

    # Checks if the deck needs reshuffling given the number of cards about to be drawn,
    #  and do so.
    def reshuffle_cards(self, num_cards=1):
        if num_cards >= len(self.deck):
            self.deck.recycle_from_pile(self.discard_pile)

    # The main loop of the game.
    # This loop continues until a player wins, or until an error occurs.
    def game_loop(self):

        # Tell everyone about the initial order of players.
        self.send_all_player_lists()

        if self.verbose:
            print("\n\n=== GAME START ===\n")

            player_string = [(f"  {x}") for x in self.players]
            print(f"Player order:")
            for p in player_string:
                print(p)
            print("\n")

        while self.in_progress:

            # Get the next player in the queue, and ask them to play a card.
            current_player = self.players.popleft()
            played_card = current_player.perform_move(self.discard_pile.top)

            # Handle the card played by the player.
            self.handle_card(played_card, current_player)
            self.send_all_player_lists()

            # Check if the current player has won.
            # If so, notify the winner, and end the game loop.
            if current_player.cards_left == 0:
                self.in_progress = False
                if self.verbose:
                    input(f"Player {current_player} has won!\n<Press ENTER to close>)")
                else:
                    #print(f"Player {current_player} has won!")
                    pass
                return current_player

    # Play the given card.
    # This will perform special moves if the given card warrants them.
    # Throws an exception if the given card is invalid.
    def handle_card(self, card, player):
        
        # If the card is None, do draw card logic
        if card is None:
            self.reshuffle_cards()
            drawn_card = self.deck.draw(1)
            if player.request_draw(drawn_card[0], self.discard_pile.top):
                card = drawn_card[0]
            else:
                self.notify_all_players(None, self.discard_pile.top, player)
                player.give_card(drawn_card)
                self.players.append(player)
                return

        # If the card is special, run it's specific function.
        # These functions are responsible for putting the player back on the queue.
        if card.special:
            self.special_methods[card.card_type](card, self.discard_pile.top, player)
        
        # If the card isn't special, play it normally.
        else:    
            self.notify_all_players(card, self.discard_pile.top, player)
            self.players.append(player)

        # Check if the card is valid, and play if it is.
        if not card.same(self.discard_pile.top) and card.card_type != CardType.WILD and card.card_type != CardType.DRAW_FOUR:
            raise ValueError(f"Player played card that does not match the top card! selected:{card} top:{self.discard_pile.top}")
        self.discard_pile.add_card(card)

    # Skips the next player in the queue.
    def skip(self, card, top_card, player):
        skipped_player = self.players.popleft()
        self.notify_all_players(card, top_card, player, msg=f"Player {skipped_player} has been skipped.")
        player.send_msg(f"Player {skipped_player} has been skipped.")
        skipped_player.notify(card, top_card, player, len(self.deck), msg=f"You have been skipped.")
        self.players.append(player)
        self.players.append(skipped_player)

    # Reverses the order of the game.
    # The message includes the new turn order of the game.
    def reverse(self, card, top_card, player):

        # Reverse the players in the queue.
        self.players.reverse()
        
        # Create the notification string for all players.
        player_string = ""
        for p in self.players:
            player_string += p.__str__() + "\n"
        player_string += player.__str__() + "\n"
        msg = (f"The turn order has been reversed!\n"
               f"Player order:\n{player_string}")
        self.notify_all_players(card, top_card, player, msg=msg)
        player.send_msg(msg)
        
        # Add the player back onto the deck.
        # If there are only two players in the game, reverse cards are treated as skip cards.

        self.players.append(player)
        if len(self.players) == 2:
            self.players.append(self.players.popleft())

    # Gives two cards to the next player in the queue.
    # Also skips that player, as per the rules.
    def draw_two(self, card, top_card, player):

        # Get the player drawing the cards.
        drawing_player = self.players.popleft()

        # Give the current player two cards.
        self.reshuffle_cards(num_cards=2)
        drawing_player.give_card(self.deck.draw(2))  

        # Tell all players about the cards drawn.
        self.notify_all_players(card, top_card, player, msg=f"{drawing_player} has drawn two cards, and has been skipped.")
        player.send_msg(f"{drawing_player} has drawn two cards, and has been skipped.")
        drawing_player.notify(card, top_card, player, len(self.deck), msg="You have drawn two cards, and have been skipped.")
      
        # Skip the drawing player.
        self.players.append(player)
        self.players.append(drawing_player)

    def draw_four(self, card, top_card, player):
        drawing_player = self.players.popleft()
        
        # Ask if the drawing player wants to challenge the Draw Four card.
        is_challenging = drawing_player.request_challenge(player, top_card)

        if is_challenging:
            
            # Show the player the opponent's hand.
            drawing_player.challenged_hand(player, player.hand)
            
            # Check if the challenge is successful.
            challenge_success = False
            for c in player.hand:
                if c.same(self.discard_pile.top) and c.card_type != CardType.DRAW_FOUR:
                    challenge_success = True
                    break
            
            # If the challenge is successful, give the current player 6 cards,
            #  and put the drawing player back on the queue.
            if challenge_success:
                
                # Give the player four cards.
                self.reshuffle_cards(num_cards=4)
                player.give_card(self.deck.draw(4))

                # Tell all non-involved players about the challenge results.
                msg = (f"Player {drawing_player}  has challenged Player {player}'s Draw Four, and succeeded!\n"
                       f"Player {player} has drawn four cards.")
                
                # Tell the drawing player about the challenge results.
                self.notify_all_players(card, top_card, player, msg=msg)
                drawing_player.notify(card, top_card, player, len(self.deck), msg=f"Your challenge against {player} was successful!")
                
                # Tell the current player that the challenge occured and succeeded.
                player.send_msg(f"Your DRAW FOUR was challenged by {drawing_player}, and succeded!\nYou have drawn four cards.")
                
                # Add the players back onto the queue.
                self.players.insert(0, drawing_player)
                self.players.append(player)

            else:
                
                # Tell all non-involved players about the challenge results.
                msg = (f"Player {drawing_player}  has challenged Player {player}'s Draw Four, and failed.\n"
                       f"Player {drawing_player} has drawn six cards, and has been skipped.")
                
                # Give the drawing player six cards.
                self.reshuffle_cards(num_cards=6)
                drawing_player.give_card(self.deck.draw(6))  

                # Tell the drawing player about the challenge results.
                self.notify_all_players(card, top_card, player, msg=msg)
                drawing_player.notify(card, top_card, player, len(self.deck), msg=f"Your challenge against {player} was a failure.\nYou have drawn six cards, and have been skipped.")
                
                # Tell the current player that the challenge occured and failed.
                player.send_msg(f"Your DRAW FOUR was challenged by {drawing_player}, but the challenge failed.\nPlayer {drawing_player} has drawn six cards, and has been skipped.") 
                
                # Add the players back onto the queue.
                self.players.insert(0, drawing_player)
                self.players.append(player)

        else:

            # Give the drawing player 4 cards, and make sure they are skipped.
            self.reshuffle_cards(num_cards=4)
            drawing_player.give_card(self.deck.draw(4))     

            # Tell all players about the card played.
            self.notify_all_players(card, top_card, player, msg=f"Player {drawing_player} has drawn four cards, and has been skipped.")
            player.send_msg(f"Player {drawing_player} has drawn four cards, and has been skipped.")
            drawing_player.notify(card, top_card, player, len(self.deck), msg="You have drawn four cards, and have been skipped.")

            # Skip the drawing player.  
            self.players.append(player)
            self.players.append(drawing_player)
    
    # Plays the card regardless of the top card.
    def wild(self, card, top_card, player):
        self.notify_all_players(card, top_card, player, msg=f"Player {player} has changed the color to {card.card_color}.")
        player.send_msg(f"You have changed the color of the pile to {card.card_color}")
        self.players.append(player)
