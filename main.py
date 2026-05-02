# Project: Battleship
# Course: CSC 520
# Group 4
# Team Members: Bhavana Chappidi (bchappi), and Mia Glenn (mglenn2)
# 
# Runs hundreds of games per agent and collects our stats (average shots, best/worst, standard deviation).


from game import run_experiment, print_results
from random_agent import RandomAgent
from hill_climbing_agent import HillClimbingAgent
from csp_agent import CSPAgent

def main():
    num_games = 500

    print("Running Battleship AI experiment...")
    print(f"Number of games per agent: {num_games}")

    random_stats = run_experiment(RandomAgent, num_games)
    hill_stats = run_experiment(HillClimbingAgent, num_games)
    csp_stats = run_experiment(CSPAgent, num_games)

    print_results("Random Agent", random_stats)
    print_results("Hill Climbing Agent", hill_stats)
    print_results("CSP + Informed Search Agent", csp_stats)

if __name__ == "__main__":
    main()