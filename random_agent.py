# Agent 1, the random baseline.

import random
from board import BOARD_SIZE

class RandomAgent:
    """
    Random baseline agent.
    It randomly shoots any cell that has not been chosen before.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Reset the agent before a new game starts.
        """
        self.available_shots = set()

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.available_shots.add((row, col))

    def choose_shot(self, board):
        """
        Pick a random untried cell.
        """
        shot = random.choice(list(self.available_shots))
        self.available_shots.remove(shot)
        return shot

    def update(self, row, col, result, sunk_ship):
        """
        Random agent does not learn from feedback.
        """
        pass