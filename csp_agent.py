# Agent 3, CSP + informed search.

import random
from board import BOARD_SIZE, SHIPS

class CSPAgent:
    """
    CSP + informed search agent.
    It uses known hits and misses to estimate where ships are most likely to be.
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

        self.hits = set()
        self.misses = set()
        self.sunk_ships = set()

    def choose_shot(self, board):
        """
        Choose the cell that appears most often in valid ship placements.
        """
        remaining_ships = []

        for ship_name in SHIPS:
            if ship_name not in self.sunk_ships:
                remaining_ships.append(ship_name)

        # If there is no useful information, use probability counting.
        scores = self._build_probability_grid(remaining_ships)

        best_score = -1
        best_cells = []

        for cell in self.available_shots:
            row, col = cell
            score = scores[row][col]

            if score > best_score:
                best_score = score
                best_cells = [cell]
            elif score == best_score:
                best_cells.append(cell)

        # If many cells tie, choose randomly among the best ones.
        shot = random.choice(best_cells)
        self.available_shots.remove(shot)
        return shot

    def update(self, row, col, result, sunk_ship):
        """
        Store feedback from the board.
        """
        if result == "miss":
            self.misses.add((row, col))

        elif result == "hit":
            self.hits.add((row, col))

        elif result == "sunk":
            self.hits.add((row, col))
            if sunk_ship is not None:
                self.sunk_ships.add(sunk_ship)

    def _build_probability_grid(self, remaining_ships):
        """
        Count how many valid ship placements include each cell.
        Higher count means the cell is more likely to contain a ship.
        """
        scores = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        for ship_name in remaining_ships:
            ship_size = SHIPS[ship_name]
            placements = self._get_valid_placements(ship_size)

            for placement in placements:
                for row, col in placement:
                    if (row, col) in self.available_shots:
                        scores[row][col] += 1

        return scores

    def _get_valid_placements(self, ship_size):
        """
        Generate all valid placements for a ship of a certain size.
        A placement is valid if:
        - it stays on the board
        - it does not include known misses
        - it is still possible based on known information
        """
        placements = []

        # Horizontal placements
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE - ship_size + 1):
                cells = []
                for i in range(ship_size):
                    cells.append((row, col + i))

                if self._placement_is_valid(cells):
                    placements.append(cells)

        # Vertical placements
        for row in range(BOARD_SIZE - ship_size + 1):
            for col in range(BOARD_SIZE):
                cells = []
                for i in range(ship_size):
                    cells.append((row + i, col))

                if self._placement_is_valid(cells):
                    placements.append(cells)

        return placements

    def _placement_is_valid(self, cells):
        """
        Check if a possible ship placement breaks any known rule.
        """
        # A ship cannot be placed on a known miss.
        for cell in cells:
            if cell in self.misses:
                return False

        # If we already have hits, prefer placements that explain at least one hit.
        # This keeps the agent focused once it has found a ship.
        if len(self.hits) > 0:
            touches_hit = False

            for cell in cells:
                if cell in self.hits:
                    touches_hit = True

            if not touches_hit:
                return False

        return True