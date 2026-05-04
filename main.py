# Project: Battleship
# Course: CSC 520
# Group 4
# Team Members: Bhavana Chappidi (bchappi), and Mia Glenn (mglenn2)
# 
# Runs hundreds of games per agent and collects our stats (average shots, best/worst, standard deviation).

from board import Board
from game import Game, run_experiment, print_results
from random_agent import RandomAgent
from hill_climbing_agent import HillClimbingAgent
from csp_agent import CSPAgent

def show_sample_game(agent_class):
    """
    Play one demo game and display the initial board and final board.
    """
    agent = agent_class()
    game = Game(agent)

    agent_name = agent_class.__name__

    print(f"Sample Game - {agent_name}")

    # Displays the board layout.
    print(f"Initial ship layout (S = ship):\n")
    game.board.display(show_ships=True)

    # Play the full game.
    shots = game.play()

    # Show the board after the game.
    print(f"\nFinal board after {shots} shots (X = hit, O = miss):\n")
    game.board.display(show_ships=False)

def main():
    num_games = 500

    # Displays one sample game with the specified agent so the board is visible.
    show_sample_game(CSPAgent)  # you can change the agents here (RandomAgent, HillClimbingAgent, or CSPAgent)

    print("\nRunning Battleship AI experiment...")
    print(f"Number of games per agent: {num_games}")

    random_stats = run_experiment(RandomAgent, num_games)
    hill_stats = run_experiment(HillClimbingAgent, num_games)
    csp_stats = run_experiment(CSPAgent, num_games)

    print_results("Random Agent", random_stats)
    print_results("Hill Climbing Agent", hill_stats)
    print_results("CSP + Informed Search Agent", csp_stats)

if __name__ == "__main__":
    main()