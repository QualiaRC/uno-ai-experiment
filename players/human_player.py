from player import Player

class HumanPlayer(Player):

    def __init__(self, name):
        self.name = name
    
    def perform_move(self, card):
        self.print_line()

        

    def notify(self, card, player, msg=None):
        self.print_line()
        print(f"Player {player} is making a move..")

    def print_line(self):
        print('================================================================================')

    def print_line_thin(self):
        print('--------------------------------------------------------------------------------')