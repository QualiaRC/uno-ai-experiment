from uno.players.human_player import HumanPlayer
from uno.players.random_ai import RandomPlayer
from uno.players.minimax_player import MinimaxPlayer
from uno.match import Match
from time import time

from collections import deque
from itertools import combinations

"""
FUNCTION NAMES:
Draw2Priority:  Value Draw2 cards highly
SkipPriority:  Value Skip cards highly
DiscardPriority:  Value discarding a card highly
WildDelay:  Deprioritize Wild cards
Draw4Delay:  Deprioritize Draw 4 cards
AttackLow:  Benefit all players if a player with low cards has been skipped or card drawn.
"""

def run_tests(num_players, num_runs):
    functions = [
        "Draw2Priority",
        "SkipPriority",
        "DiscardPriority",
        "WildDelay",
        "Draw4Delay",
        "AttackLow"
    ]
    
    player_names = ["VARIABLE_MINIMAX"]
    player_names += [f"BEST_MINIMAX_{x+1}" for x in range(num_players - 1)]
    
    function_runs = function_combinations(functions)
    current_best_heuristics = function_runs[0]

    t0 = time()
    for function_set in function_runs:

        print("\n" + ("=" * 80))
        print("Starting new test with function set:")
        for function in function_set:
            print(f" | {function}")
        
        # Variable player gets new function set
        player_list = [MinimaxPlayer(player_names[0], player_names, function_set)]

        # Set up best players
        for i in range(num_players - 1):
            player_list += [MinimaxPlayer(player_names[i + 1], player_names, current_best_heuristics)]

        # Set up win counter
        wincount = dict()
        for player in player_names:
            wincount[player] = 0

        # Set up and start match
        t = time()
        for i in range(num_runs):
            match = Match(deque(player_list), verbose=False)
            wincount[match.winner.name] += 1

        print("\nStatistics:")
        print(f" {wincount}")
        print(f" Minimax's win-rate: {round(wincount['VARIABLE_MINIMAX'] / num_runs * 100, 2)}%")
        print(f" Time taken: {round(time() - t, 3)} seconds")

        new_best = False
        for i in range(num_players - 1):
            if wincount["VARIABLE_MINIMAX"] > wincount[player_names[i + 1]]:
                new_best = True

        if new_best:
            print(f"\n .{('-' * 33)}.")
            print(" | ! New best function set found ! |")
            print(f" '{('-' * 33)}'")
            current_best_heuristics = function_set

    # Congratulations on waiting a million years to get here!
    print(("=" * 80))
    print("DONE TESTING")
    print(f"Total time taken: {round(time() - t0, 3)} seconds")
    print(("=" * 80))


# Get all combinations of a list without repeats
#  e.g. [1, 2, 3] returns [[1],[2],[3],[1, 2],[1, 3],[2, 3],[1, 2, 3]]
def function_combinations(functions):
    function_runs = [[]]
    for i in range(len(functions)):
            for combination in combinations(functions, i + 1):
                function_runs += [list(combination)]
    return function_runs


if __name__ == "__main__":
    run_tests(2, 100)
