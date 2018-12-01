class DiscardPile(list):

    # Gets the top card of the discard pile.
    @property
    def top(self):
        return self[len(self)-1]

    # Adds a card to the discard pile.
    def add_card(self, card):
        self.append(card)

    