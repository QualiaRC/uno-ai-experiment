from uno.game_components.card import *

from copy import copy

class Heuristics:
    
    def __init__(self, player_name, players, functions):
        self.player_name = player_name
        self.players = players
        self.player_count = len(self.players)
        self.current_player_order = None
        self.hand = None
        self.cards_played = None
        self.mystery_hands = {}
        self.card_history = None
        self.applied_functions = functions
        self.functions = { 
            "Draw2Priority": self.l_drawtwo, 
            "SkipPriority": self.l_skip, 
            "DiscardPriority": self.l_hasdiscarded,
            "WildDelay": self.l_wrongwild,
            "Draw4Delay": self.l_wrongdrawfour,
            "AttackLow": self.l_attacklow
        }        

    #Card history is list [asdfa]
    def update(self, card_history):
        self.card_history = card_history

    def get_value(self):
        ret = [0 for _ in range(self.player_count)]

        for function in self.applied_functions:
            values = self.functions[function](self.card_history)
            for i in range(len(ret)):
                ret[i] += values[i]

        return ret

    def l_attacklow(self, card_history):
        
        # Get initial hand counts.
        ret = [0 for _ in range(self.player_count)]
        for i in range(len(self.players)):
            ret[i] += len(self.mystery_hands[self.players[i]])

        # Get hand counts after the round is over.
        player_order = copy(self.current_player_order)
        for card in card_history:
            if card[1] == None:
                continue
            if card[0].card_type == CardType.SKIP or card[0].card_type == CardType.DRAW_TWO or card[0].card_type == CardType.DRAW_FOUR:
                player_order.append(player_order.pop(0))
                if len(self.mystery_hands[player_order[0]]) < 7:
                    for player in self.players:
                        if player != player_order[0]:
                            ret[self.players.index(player)] += (7 - len(self.mystery_hands[player_order[0]]))
                player_order.append(player_order.pop(0))
            elif card[0].card_type == CardType.REVERSE:
                player_order.reverse()
            else:
                player_order.append(player_order.pop(0))

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
            if card[1] == self.player_name and card[0].card_type == CardType.WILD:
                cc = self.color_count(self.hand)
                optimal_color = max(cc, key=cc.get)
                if card[0].card_color != optimal_color:
                    ret[self.players.index(card[1])] -= 2
                else:
                    ret[self.players.index(card[1])] -= 1    
        return ret

    def l_wrongdrawfour(self, card_history):
        ret = [0 for _ in range(self.player_count)]
        for card in card_history:
            if card[1] == self.player_name and card[0].card_type == CardType.DRAW_FOUR:
                cc = self.color_count(self.hand)
                optimal_color = max(cc, key=cc.get)
                if card[0].card_color != optimal_color:
                    ret[self.players.index(card[1])] -= 4
                else:
                    ret[self.players.index(card[1])] -= 3    
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