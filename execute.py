from uno.players.human_player import HumanPlayer
from uno.players.random_ai import RandomPlayer
from uno.players.minimax_player import MinimaxPlayer
from uno.match import Match

from collections import deque

if __name__ == "__main__":
    #player_list = [HumanPlayer("BEAN"), RandomPlayer("COM1"), RandomPlayer("COM2"), RandomPlayer("COM3")]
    #player_list = [HumanPlayer("BEAN"), RandomPlayer("COM1")]
    #player_list = [RandomPlayer("RANDOM"), MinimaxPlayer("MINIMAX", ["RANDOM", "MINIMAX"])]
    #player_list = [MinimaxPlayer("GREEN BEAN", ["GREEN BEAN", "COFFEE BEAN"]), MinimaxPlayer("COFFEE BEAN", ["GREEN BEAN", "COFFEE BEAN"])]
    #player_list = [HumanPlayer("BEAN"), MinimaxPlayer("MinimaxCOM1", ["BEAN", "MinimaxCOM1"])]
    #Match(deque(player_list))

    #wincount = {"RANDOM1": 0, "MINIMAX": 0, "RANDOM2": 0}
    wincount = {"RANDOM": 0, "MINIMAX": 0}

    for i in range(1000):
        #player_list = [RandomPlayer("RANDOM1"), RandomPlayer("RANDOM2"), MinimaxPlayer("MINIMAX", ["RANDOM1", "RANDOM2", "MINIMAX"])]
        player_list = [RandomPlayer("RANDOM"), MinimaxPlayer("MINIMAX", ["RANDOM", "MINIMAX"])]
        m = Match(deque(player_list), verbose=False)
        wincount[m.winner.name] += 1

    print(wincount)
#    for _ in range(1000):
#        player_list = [ MinimaxPlayer("MINIMAX1", ["MINIMAX1", "MINIMAX2"]), MinimaxPlayer("MINIMAX2", ["MINIMAX1", "MINIMAX2"])]
#        Match(deque(player_list), verbose=False)
