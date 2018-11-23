import sys
sys.path.append('./cards')

from deck import Deck
from pile import Pile
from random import randint
from player import Player
from random import shuffle

class Match():

    def __init__(self, player_count):
        
        names = ["Amy", "Alex", "Dr. Retsemem", "Dr. Eggman"]
        shuffle(names)

        self.in_progress = True
        self.direction = "clockwise"

        # Create a new deck full deck and empty pile
        self.deck = Deck()
        self.pile = Pile()
        self.pile.place_card(self.deck.draw_card())

        # Set up players
        self.players = list()
        self.player_count = player_count
        for i in range(player_count - 1):
            self.players.append(Player(names.pop(), "basic", self))
        self.players.append(Player("Ryan", "player", self))
        shuffle(self.players)

        # Print player order
        print(f'\nPlayer order: {[str(x.name) for x in self.players]}\n')

        # Deal cards to each player
        for i in range(5):
            for player in self.players:
                player.draw_card(self.deck)

        while(self.in_progress):
            # Current player performs turn
            self.players[0].perform_move(self.pile)

            # Set next player
            self.next_player()

            # Check if any players have 0 cards in their hand
            for player in self.players:
                if len(player.hand) == 0:
                    self.in_progress = False
                    input(f'Player {player.name} has won!\n<Press ENTER to close>')
                    return

            # Prints
            for i in range(4):
                print()

    def reverse(self):
        if self.direction == "clockwise":
            self.direction = "counterclockwise"
        else:
            self.direction = "clockwise"

    def next_player(self):
        if self.direction == "clockwise":
            self.players.append(self.players.pop(0))
        else:
            self.players.insert(0, self.players.pop())

    def skip(self):
        self.next_player()
        print(f'Player {self.players[0]} is getting skipped.\n')
