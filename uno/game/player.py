import sys
sys.path.append('./cards')

from deck import Deck
from card import Color

class Player():

    def __init__(self, name, player_type, match):
        self.name = name
        self.player_type = player_type
        self.hand = list()
        self.match = match

    def draw_card(self, deck):
        self.hand.append(deck.draw_card())

    def play_card(self, index, pile):
        # Check if valid card
        if self.hand[index].matches_card(pile.get_top_card()):
            # if wild card, prompt user for color
            if self.hand[index].color.value == Color.WILD:
                valid = False
                while not valid:
                    chosen_color = input("Select a color (1. Red, 2. Green, 3. Yellow, 4. Blue): ")
                    if chosen_color < 5 and chosen_color > 0:
                        self.hand[index].color = Color(chosen_color)
                    else: 
                        print("Must pick a number between 1 and 4")
                
            # if skip card, call skip
            if self.hand[index].card_type.value == 11:
                self.match.skip()
                
            # if reverse card, call reverse
            if self.hand[index].card_type.value == 12:
                self.match.reverse()

            pile.place_card(self.hand.pop(index))
            return True

        print("Card cannot be played.")
        return False

    def perform_move(self, pile):
        self.print_line()
        print(f'Player: {self.name} is making a move')
        self.print_line_thin()
        if self.player_type == "player":
            print(f'Top Card : ', end='')
            pile.get_top_card().print_card()
            print()
            self.print_hand()

            waiting = True
            while(waiting):
                user_input = input("Enter a command: ").lower().split()
                    
                if len(user_input) > 2 or len(user_input) == 0:
                    print('Invalid command. Type "help" for a list of commands.\n')
                    continue
                command = user_input[0]
                if len(user_input) == 2:
                    param = user_input[1]    
                
                if command == "skip":
                    waiting = False
                elif command == "play":
                    if self.check_int(param):
                        if int(param) >= len(self.hand) or int(param) < 1:
                            print("Invalid card number.\n")
                            continue
                        waiting = not self.play_card(int(param) - 1, pile)
                else:
                    print('Invalid command. Type "help" for a list of commands.\n')

        elif self.player_type == "basic":
            # TODO: basic AI makes move
            print()

        elif self.player_type == "advanced":
            # TODO: advanced AI makes move
            print()

        print(f'Player: {self.name} has finished their move')
        self.print_line()
        print()

    def print_hand(self):
        for i in range(len(self.hand)):
            print(f'Card {i+1} : ', end='')
            self.hand[i].print_card()
        print()

    def print_line(self):
        print('================================================================================')

    def print_line_thin(self):
        print('--------------------------------------------------------------------------------')

    def check_int(self, obj):
        try:
            int(obj)
            return True
        except ValueError:
            print("Invalid number")
            return False