import sys
sys.path.append("../game_components")

from player import Player
from card import CardType
from card import CardColor
class HumanPlayer(Player):

    def __init__(self, name):
        self.name = name
        self.color_conversion = {
            "red": CardColor.RED,
            "blue": CardColor.BLUE,
            "green": CardColor.GREEN,
            "yellow": CardColor.YELLOW
        }
    
    def perform_move(self, top_card):
        self.print_line()
        
        # Print out player's cards.
        print("Your cards:")
        ptr = 0
        for card in self.hand:
            ptr += 1
            if card == top_card:
                print(f"\t>{ptr}. {card}")
            else:
                print(f"\t{ptr}. {card}")
        
        print(f"Current top card: {top_card}")
        
        # Request a play from the player.
        player_turn = True
        card = None
        while player_turn:
            
            # Get a number from the player
            q = input(f"Select a card to play. (1 to {ptr}")
            value = None
            try:
                value = int(q)
            except:
                print("Invalid input!")
                continue
            
            # Check if input is in range.
            if value < 1 or value > ptr:
                print("Input out of range!")
                continue

            # Check if card is a valid card to play.
            if self.hand[value-1] != top_card:
                print("Card does not match the top card!")
                continue

            # Check if card being played is a wild card, and handle that case.
            if (self.hand[value-1].card_type == CardType.WILD or
               self.hand[value-1].card_type == CardType.DRAW_FOUR):
                q = input("Select color for the wildcard.")
                if not q.lower() in self.color_conversion:
                    print("Invalid color!")
                card = self.hand.pop(value-1)
                card.card_color = self.color_conversion[q.lower()]
                player_turn = False
            else:
                card = self.hand.pop(value-1)
                player_turn = False
        
        # Play the card.
        print(f"Playing the {card} card.")
        return card

    def notify(self, card, player, msg=None):
        self.print_line()
        print(f"Player {player} is making a move..")
        print(f"Player {player} has played a {card}.")
        if msg:
            print(msg)
        self.print_line_thin()

    def request_draw(self, card, top_card):
        print(f"You have drawn the {card} card.")
        if card != top_card:
            return False
        else:
            q = input("Play this card? (y/n)")
            return q.lower() == "y"

    def request_challenge(self, player):
        print(f"Player {player} has played a Draw Four card on you.")
        q = input("Challenge the card? (y/n)")
        return q.lower() == "y"

    def challenged_hand(self, player, cards):
        print(f"Player {player} has revealed their hand to you:")
        for card in cards:
            print(f"\t{card}")

    def print_line(self):
        print('================================================================================')

    def print_line_thin(self):
        print('--------------------------------------------------------------------------------')