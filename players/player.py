class Player:

    # The base Player has a name, and an empty list as a hand.
    def __init__(self, name):
        self.name = "DEFAULT"
        self.hand = list()

    # Gets the number of cards in the player's hand.
    @property
    def cards_left(self):
        return len(self.hand)

    # Adds a given list of cards to the player's hand.
    def give_card(self, cards : list):
        self.hand += cards

    # Makes the player perform a move given the top card of the discard pile.
    # Returns the card the player wants to play, or None if the player cannot play a card.
    # perform_move is responsible for checking whether the card returned is valid or not.
    # The card returned should be removed from the player's hand before returning.
    def perform_move(self, card):
        raise NotImplementedError

    # Called by Match every turn to update the player about the game.
    # Arguments include a card and the player playing the card.
    # msg, if passed, includes special information about the game,
    #  including skips, reversals, etc.
    def notify(self, card, player, msg=None):
        raise NotImplementedError

    # Called by Match in the case where the player does not play a card from their hand,
    #  whether it be due to the inability or choice to do so.
    # Returns True or False, depending on whether the player decides to play the given card.
    # request_draw is responsible for checking whether the card can be played or not.
    def request_draw(self, card):
        raise NotImplementedError

    # Called by Match in the case of a Draw Four card being played, 
    #  given the player who played the Draw Four card.
    # The player who has to draw four can challenge the Draw Four card,
    #  forcing the opponent who played the Draw Four card to reveal their hand.
    #    - If the opponent could have played something other than the Draw Four,
    #      that opponent draws four instead of the player, and the player is not skipped.
    #    - Otherwise, the player draws six instead of four.
    # Returns True or False, depending on whether the player wants to issue the challenge.
    def request_challenge(self, player):
        raise NotImplementedError

    # Called by Match when a challenge is issued, showing the cards of the challenged player.
    def challenged_hand(self, player, cards):
        raise NotImplementedError

    def __str__(self):
        return self.name