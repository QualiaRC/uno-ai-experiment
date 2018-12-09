from uno.game_components.deck import Deck

from collections import Counter
from copy import copy

class Node:

    def __init__(self, depth, card, player):
        
        # Children are represented in a tuple as (Child, weight)
        self.children = list()
        self.value = None
        self.depth = depth
        self.card = card
        self.player = player


class Minimax:

    def __init__(self, number_of_players):
        self.all_cards = Deck()
        self.cards_played = list()
        self.number_of_players = number_of_players
    
    @property
    def possible_cards(self):
        return Counter([card for card in self.all_cards if not (card in self.cards_played)])

    def apply_heuristics(self, node):
        node.value = tuple(0 for _ in range(self.number_of_players))

    def asdf(self):
        pass

    def generate_tree(self, parent_cards, players, depth=None):
        
        depth_limit = self.number_of_players * 2

        # If no depth is passed, start generating the tree at node 0.
        if depth is None:
            depth = 0

        # Create the node for the current level.
        current_node = Node(depth, parent_cards[len(parent_cards)-1])

        # If we have hit depth limit, return the node.
        if depth >= depth_limit:
            self.apply_heuristics(current_node)
            return current_node

        # Get all possible cards for the following depth.
        playable_cards = self.possible_cards

        # Create children nodes for each possible card.
        new_depth = depth + 1
        for card in playable_cards:
            new_parent_cards = copy(parent_cards) + [card] # deepcopy?
            weight = playable_cards[card]
            current_node.children += [(self.generate_tree(new_parent_cards, depth=new_depth), weight)]

        # Return the working node after generating children.
        return current_node