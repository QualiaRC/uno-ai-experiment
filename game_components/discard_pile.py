class DiscardPile(list):

    # Gets the top card of the discard pile.
    @property
    def top(self):
        if len(self) > 0:
            return self[len(self)-1]
        else:
            return None

    # Adds a card to the discard pile.
    def add_card(self, card):
        self.append(card)

    