# The game engine that runs a single game (handles shots, feedback, win detection).

from board import Board, SHIPS

class Game:
    """
    Runs a single game of Battleship between an agent and a board.
    The agent picks where to shoot, the board says hit/miss/sunk, and the game keeps going until every ship is sunk.
    """
    def __init__(self, agent):
        # Create a fresh board with randomly placed ships.
        self.board = Board()

        # The agent that will decide where to shoot.
        self.agent = agent

        # Count how many shots the agent takes to win.
        self.shot_count = 0

    def play(self):
        """
        Play one full game. The agent shoots until all ships are sunk.
        Returns the total number of shots it took to win.
        """
        # Give the agent a fresh start for this game.
        self.agent.reset()

        while not self.board.all_ships_sunk():
            # Ask the agent to pick a cell to shoot.
            row, col = self.agent.choose_shot(self.board)

            # Fire the shot and get the result.
            result = self.board.take_shot(row, col)
            self.shot_count += 1

            # Figure out which ship was sunk (if any)
            sunk_ship = None
            if result == "sunk":
                # Find which ship just got sunk by checking what's on that cell.
                sunk_ship = self.board.grid[row][col]
            
            # Tell the agent what happened so it can update its strategy.
            self.agent.update(row, col, result, sunk_ship)

        return self.shot_count
    
def run_experiment(agent_class, num_games=500):
    """
    Run many games with the same type of agent and collect stats.
    Args:
        agent_class: the agent class to test (e.g., RandomAgent).
        num_games: How many games to simulate (default 500).
    Returns a dictionary with:
        - average: mean shots to win across all games
        - best: fewest shots in any game
        - worst: most shots in any game
        - std_dev: how consistent the agent is
        - all_results: list of every game's shot count
    """
    results = []

    for i in range(num_games):
        # Create a new agent and a new game each time.
        agent = agent_class()
        game = Game(agent)
        shots = game.play()
        results.append(shots)

    # Calculate the stats
    average = sum(results) / len(results)
    best = min(results)
    worst = max(results)

    # Standard deviation (how spread out the results are).
    variance = sum((x - average) **2 for x in results) / len(results)
    std_dev = variance ** 0.5

    return {
        "average": round(average, 2),
        "best": best,
        "worst": worst,
        "std_dev": round(std_dev, 2),
        "all_results": results
    }

def print_results(agent_name, stats):
    """
    Print the experiment results in a clean table row.
    """
    print(f"\n {agent_name}")
    print(f" Average shots to win: {stats['average']}")
    print(f" Best game (fewest): {stats['best']}")
    print(f" Worst game (most): {stats['worst']}")
    print(f" Standard deviation: {stats['std_dev']}")