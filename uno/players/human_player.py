from uno.players.player import Player
from uno.game_components.card import CardType
from uno.game_components.card import CardColor

class HumanPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.color_conversion = {
            "red": CardColor.RED,
            "blue": CardColor.BLUE,
            "green": CardColor.GREEN,
            "yellow": CardColor.YELLOW
        }
    
    # Prints the player's hand.
    def print_hand(self, top_card):
        print("Your cards:")
        ptr = 0
        for card in self.hand:
            ptr += 1
            if card == top_card:
                print(f"\t>{ptr}. {card}")
            else:
                print(f"\t{ptr}. {card}")

    # Asks the player to select a color for their wild card.
    # Returns True on selection, or False if the player decides not to play the card.
    def select_wild_color(self, card):
        while(True):  # mmmmmmMMMMMMMAAAAAAAAAAAAAAAMAAAAAAAAAAAAAAAAaaaAAAAA
            q = input("Select color for the wildcard (Type 'cancel' to go back):  ")
            if q == "cancel":
                return False
            if q == "" or not q.lower() in self.color_conversion:
                print("Invalid input!")
                print("Valid inputs:\n  red\n  blue\n  green\n  yellow\n  cancel")
                continue
            card.card_color = self.color_conversion[q.lower()]
            return True
    
    # Get a move from the player.
    def perform_move(self, top_card):

        print(f"== PLAYER TURN: {self.name} - TOP CARD: {top_card} ==")
        
        # Request a play from the player.
        player_turn = True
        card = None
        while player_turn:

            # Print the player's hand.
            self.print_hand(top_card)

            # Get a number from the player.
            # If there is no play to be made, or the player does not want to play, return None.
            q = input(f"Select a card to play. (1 to {len(self.hand)}) ('skip' to not play a card):  ")
            if [x for x in self.hand if x == top_card] == [] or q == "skip":
                return None

            # Attempt to convert the input into an integer.
            value = None
            try:
                value = int(q)
            except:
                print("Invalid input!")
                continue

            # Check if input is in range.
            if value < 1 or value > len(self.hand):
                print("Input out of range!")
                continue

            # Check if card is a valid card to play.
            if self.hand[value-1] != top_card:
                print("Card does not match the top card!")
                continue

            # Pull out the requested card.
            card = self.hand.pop(value-1)

            # Check if card being played is a wild card, and handle that case.
            if (card.card_type == CardType.WILD or
               card.card_type == CardType.DRAW_FOUR):
                if not self.select_wild_color(card):  # User canceled the wild card choice.
                    self.hand.append(card)
                else:
                    player_turn = False
            else:
                player_turn = False
        
        # Play the card.
        print(f"Playing the {card} card.")
        print()
        print()
        return card

    def notify(self, card, top_card, player, deck_total, msg=None):
        
        print(f"== PLAYER {player}'s TURN (with {player.cards_left} remaining) - TOP CARD: {top_card} ==")
        if card is None:
            print(f"  Player {player} has drawn a card, and played nothing.")
        else:
            print(f"  Player {player} has played a {card}.")
        if msg:
            print("  " + msg)
        print()

    def request_draw(self, card, top_card):
        
        print(f"  You have drawn the {card} card.")
        if card != top_card:  # Card is unplayable.
            print()
            print()
            return False
        
        # If the card is playable, ask the player if they want to play it.
        q = input("  Play this card? (y/n)")
        if q != "y":
            return False
        
        # If the card is a wild card, ask for the color.
        # If the user cancels selecting a card, just return False.
        if card.card_type == CardType.WILD or card.card_type == CardType.DRAW_FOUR:
            return self.select_wild_color(card)
        return True

    def request_challenge(self, player):
        print(f"  Player {player} has played a Draw Four card on you.")
        q = input("  Challenge the card? (y/n)")
        return q.lower() == "y"

    def challenged_hand(self, player, cards):
        print(f"  Player {player} has revealed their hand to you:")
        for card in cards:
            print(f"\t{card}")

    def send_msg(self, msg):
        print(msg)
        print()