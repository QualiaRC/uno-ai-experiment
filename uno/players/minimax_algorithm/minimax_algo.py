from uno.game_components.deck import Deck
from uno.game_components.card import *
from uno.players.minimax_algorithm.heuristics import Heuristics

from collections import Counter
from copy import copy
from copy import deepcopy
from random import choice
from random import randint

class Node:

    def __init__(self, depth, card, player_name):
        
        # Children are represented in a tuple as (Child, weight)
        self.children = list()
        self.value = []
        self.depth = depth
        self.card = card
        self.player_name = player_name


class Minimax:

    def __init__(self, player_name, players):
        self.all_cards = Deck()
        self.cards_played = list()
        self.players = players
        self.number_of_players = len(self.players)
        self.player_name = player_name
        self.hand = None
        self.heuristics = Heuristics(self.player_name, self.players)
        self.mystery_hands = dict()
        for player in players:
            self.mystery_hands[player] = [None for _ in range(7)]

    # Returns a list of (card, amt) pairs, where amt is the number of times amt appears.
    @property
    def possible_cards(self):
        cards_available = []
        for card1 in self.all_cards:
            found = False
            for card2 in self.cards_played:
                if card1 == card2:
                    found = True
                    break
            if not found:
                cards_available.append(card1)
        card_count = []
        for card in cards_available:
            new_card = True
            for card_tuple in card_count:
                if card_tuple[0] == card:
                    card_tuple[1] += 1
                    new_card = False
                    break
            if new_card:
                card_count += [[card, 1]]
        return card_count
            
    def get_card(self, hand, topcard, deck_total, players, previous_player):
        if len(self.cards_played) == 0:
            self.cards_played += [deepcopy(topcard)]
        self.hand = hand
        tree = self.generate_tree([(topcard, previous_player)], deck_total, players)


        states = [x[0].value for x in tree.children]
        best_state = self.minimum_maximum(self.player_name, states)

        for child in tree.children:
            if child[0].value == best_state:
                return child[0].card
        return None

    def apply_heuristics(self, node, parent_cards):
        self.heuristics.update(self.hand, parent_cards)
        node.value = self.heuristics.get_value()

    def minimum_maximum(self, player_name, states):

        # If there are no states, return None, as no state can be selected.
        if not states:
            return None
        
        # Get the index matching the player to the states.
        index = self.players.index(player_name)

        # Make a copy of the states, and create a formatted states list for parsing.
        states_copy = deepcopy(states)
        formatted_states = [[x.pop(index), max(x)] for x in states_copy]
        
        # Find the maximum value for the player, and the minimum maximum values of the other players.
        max_value = max([x[0] for x in formatted_states])
        min_value = min([x[1] for x in formatted_states if x[0] == max_value])

        # Get all optimal choices for the player.
        minmaxes = []
        for i in range(len(formatted_states)):
            if formatted_states[i][0] == max_value and formatted_states[i][1] == min_value:
                minmaxes.append(i)

        # Return an optimal choice at random.
        # If there is only one optimal choice, this just returns the single choice.
        return states[choice(minmaxes)]

    def generate_tree(self, parent_cards, deck_total, players, depth=None):
        depth_limit = self.number_of_players

        # If no depth is passed, start generating the tree at node 0.
        if depth is None:
            depth = 0
        # Create the node for the current level.
        current_node = Node(depth, parent_cards[len(parent_cards)-1][0], players[0])
        # If we have hit depth limit or we encounter the AI player again, return the node.
        if depth == depth_limit or (current_node.player_name == self.player_name and depth != 0):
            self.apply_heuristics(current_node, parent_cards)
            return current_node

        # Get all possible cards for the following depth.
        if current_node.player_name == self.player_name:
            playable_cards = []
            for card in self.hand:
                new_card = True
                for card_pair in playable_cards:
                    if card_pair[0] == card:
                        card_pair[1] += 1
                        new_card = False
                        break
                if new_card:
                    playable_cards += [[card, 1]]
        else:
            playable_cards = self.possible_cards

        playable_cards = [x for x in playable_cards if x[0].same(current_node.card)]
        new_wilds = []
        counter_wild = 0
        counter_draw4 = 0
        for card in playable_cards:
            if card[0].card_type == CardType.WILD:
                counter_wild += 1
            if card[0].card_type == CardType.DRAW_FOUR:
                counter_draw4 += 1
                
        colors = [x for x in list(CardColor) if x != CardColor.WILD]

        for color in colors:
            if counter_wild != 0:
                new_wilds.append([Card(color, CardType.WILD), counter_wild])
            elif counter_draw4 != 0:
                new_wilds.append([Card(color, CardType.DRAW_FOUR), counter_draw4]) 

        playable_cards = [x for x in playable_cards if x[0].card_color != CardColor.WILD]
        playable_cards += new_wilds

        # Create children nodes for each possible card.
        new_depth = depth + 1
        #print(f"{current_node.player_name} depth: {depth}")
        #[print(f"playable {x[0]}") for x in playable_cards]
        #print()
        for card in playable_cards:
            # TODO: CHECK IF THE DECK IS SHUFFLED AFTER THE CARD IS PLAYED, ONCE BEFORE AND AFTER THE DRAW CONDITIONAL
            # Create a new list of players, with the order reflecting the next turn based off of the card being played.

            # TODO: UPDATE THE DECK_TOTAL
            new_deck_total = deck_total
            
            new_list = copy(players)
            if card[0].card_type == CardType.SKIP or card[0].card_type == CardType.DRAW_TWO or card[0].card_type == CardType.DRAW_FOUR:
                new_list.append(new_list.pop(0))
                new_list.append(new_list.pop(0))
            elif card[0].card_type == CardType.REVERSE:
                new_list.reverse()
            else:
                new_list.append(new_list.pop(0))


            # Get the weight of the branch being created.
            new_parent_cards = (copy(parent_cards) + [(card[0], current_node.player_name)]) # deepcopy?
            
            # Remove the card from the hand if it is the player's turn
            if current_node.player_name == self.player_name:
                for i in range(len(self.hand)):
                    if self.hand[i].same(card[0]):
                        self.hand.pop(i)
                        break
            weight = card[1]

            current_node.children += [(self.generate_tree(new_parent_cards, new_deck_total, new_list,depth=new_depth), weight)]

        # Return the working node after generating children.
        states = []
        for child in current_node.children:
            #print(f"{child[0].value} ASDF")
            val = [(x * child[1]) for x in child[0].value]
            states += [val]
        #print(f"{states}")
        current_node.value = self.minimum_maximum(current_node.player_name, states)
        return current_node