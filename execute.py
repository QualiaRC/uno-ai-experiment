from players.human_player import HumanPlayer
from players.random_ai import RandomPlayer
from match import Match
from collections import deque

if __name__ == "__main__":
    player_list = [HumanPlayer("BEAN"), RandomPlayer("COM1"), RandomPlayer("COM2"), RandomPlayer("COM3")]
    Match(deque(player_list))