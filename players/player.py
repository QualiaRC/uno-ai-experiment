class Player:

    def __init__(self, name):
        self.name = "DEFAULT"
        self.hand = list()

    @property
    def cards_left(self):
        return len(self.hand)

    def give_card(self, card):
        self.hand.append(card)

    def perform_move(self, card):
        raise NotImplementedError

    def notify(self, card, player, msg=None):
        raise NotImplementedError

    def __str__(self):
        return self.name