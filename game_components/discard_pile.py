class DiscardPile(list):

    @property
    def top(self):
        return self[len(self)-1]

    def add_card(self, card):
        self.append(card)

    