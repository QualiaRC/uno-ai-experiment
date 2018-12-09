from uno.players.player import Player

class MinimaxCardPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.name = name
    
    # Select a card by generating a decision tree, and selecting a card based on heuristic functions etc.
    def perform_move(self, top_card):
        pass

    # Handle the card given by adding it to relevant structures keeping track of cards played.
    def notify(self, card, top_card, player, msg=None):
        pass
    
    # Make a decision about whether to play a drawn card or not.
    def request_draw(self, card, top_card):
        pass

    # Make a decision about whether to challenge a Draw Four, based on the odds of the player bluffing.
    def request_challenge(self, player):
        pass

    # Handle the cards given by adding it to relevant structures keeping track of cards.
    def challenged_hand(self, player, cards):
        pass

    # Don't actually care about sent messages, do nothing.
    def send_msg(self, msg):
        pass