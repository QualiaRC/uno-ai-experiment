from uno.players.human_player import HumanPlayer
from uno.players.random_ai import RandomPlayer
from uno.players.minimax_card_player import MinimaxCardPlayer
from uno.match import Match

from collections import deque

if __name__ == "__main__":
    #player_list = [HumanPlayer("BEAN"), RandomPlayer("COM1"), RandomPlayer("COM2"), RandomPlayer("COM3")]
    #player_list = [HumanPlayer("BEAN"), RandomPlayer("COM1")]
    player_list = [RandomPlayer("RANDOM"), MinimaxCardPlayer("MINIMAX", ["RANDOM", "MINIMAX"])]
    #player_list = [MinimaxCardPlayer("GREEN BEAN", ["GREEN BEAN", "COFFEE BEAN"]), MinimaxCardPlayer("COFFEE BEAN", ["GREEN BEAN", "COFFEE BEAN"])]
    #player_list = [HumanPlayer("BEAN"), MinimaxCardPlayer("MinimaxCOM1", ["BEAN", "MinimaxCOM1"])]
    Match(deque(player_list))
