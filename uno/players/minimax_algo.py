from uno.game_components.deck import Deck

from copy import copy

class Node:

    def __init__(self, depth, card):
        
        # Children are represented in a tuple as (Child, weight)
        self.children = list()
        self.value = 0
        self.depth = depth
        self.card = card


class Minimax:

    def __init__(self, number_of_players):
        self.all_cards = Deck()
        self.cards_played = list()
        self.number_of_players = number_of_players
    
    @property
    def possible_cards(self):
        return [card for card in self.all_cards if not (card in self.cards_played)]

    def apply_heuristics(self, node):
        node.value = tuple(0 for _ in range(self.number_of_players))

    def generate_tree(self, parent_cards, depth=None, depth_limit=4):
        
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
        possible_cards = [c for c in self.possible_cards if not (c in parent_cards)]

        # Create children nodes for each possible card.
        new_depth = depth + 1
        for card in possible_cards:
            new_parent_cards = copy(parent_cards) + [card] # deepcopy?
            weights = tuple(0 for _ in range(self.number_of_players))  # TODO GENERATE WEIGHTS FOR THE CHILD
            current_node.children += [(self.generate_tree(new_parent_cards, depth=new_depth, depth_limit=depth_limit), weights)]

        # Return the working node after generating children.
        return current_node