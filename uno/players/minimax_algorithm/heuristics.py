from uno.game_components.card import *

class Heuristics:
    
    def __init__(self, player_name, players):
        self.player_name = player_name
        self.players = players
        self.player_count = len(self.players)
        self.hand = None
        self.card_history = None
        self.functions = [ 
            self.l_drawtwo, 
            self.l_skip, 
            self.l_hasdiscarded,
            self.l_wrongwild
        ]

    def update(self, hand, card_history):
        self.hand = hand
        self.card_history = card_history

    def get_value(self):
        ret = [0 for _ in range(self.player_count)]

        for f in self.functions:
            values = f(self.card_history)
            for i in range(len(ret)):
                ret[i] += values[i]

        return ret

    def l_drawtwo(self, card_history):
        ret = [0 for _ in range(self.player_count)]
        for card in card_history:
            if card[0].card_type == CardType.DRAW_TWO and not card[1] is None:
                ret[self.players.index(card[1])] += 3
        return ret

    def l_skip(self, card_history):
        ret = [0 for _ in range(self.player_count)]
        for card in card_history:
            if card[0].card_type == CardType.SKIP and not card[1] is None:
                ret[self.players.index(card[1])] += 2
        return ret

    def l_hasdiscarded(self, card_history):
        ret = [0 for _ in range(self.player_count)]
        for card in card_history:
            if not card[1] is None:
                ret[self.players.index(card[1])] += 5
        return ret

    def l_wrongwild(self, card_history):
        ret = [0 for _ in range(self.player_count)]
        for card in card_history:
            if card[1] == self.player_name and (card[0].card_type == CardType.WILD or card[0].card_type == CardType.DRAW_FOUR):
                cc = self.color_count(self.hand)
                optimal_color = max(cc, key=cc.get)
                if card[0].card_color != optimal_color:
                    ret[self.players.index(card[1])] -= 1
        return ret

    def color_count(self, hand):
        color_count = {
            CardColor.BLUE: 0,
            CardColor.RED: 0,
            CardColor.GREEN: 0,
            CardColor.YELLOW: 0
        }
        for card in hand:
            if not card.card_color == CardColor.WILD:
                color_count[card.card_color] += 1
        return color_count