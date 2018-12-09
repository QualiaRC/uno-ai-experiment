from uno.players.human_player import HumanPlayer
from uno.players.random_ai import RandomPlayer
from uno.match import Match
from collections import deque

if __name__ == "__main__":
    #player_list = [HumanPlayer("BEAN"), RandomPlayer("COM1"), RandomPlayer("COM2"), RandomPlayer("COM3")]
    player_list = [HumanPlayer("BEAN"), RandomPlayer("COM1")]
    #Match(deque(player_list))

from uno.players.minimax_algo import Minimax
asdf = Minimax("a", ["a","b","c","d"])
print(asdf.minimum_maximum("a", [[1, 2, 3, 4], [4, 3, 2, 1], [4, 3, 1, 2], [1, 1, 1, 1]]))