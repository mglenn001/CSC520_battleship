# The game board and ship placement logic.

import random

# The five ships and how many cells each one takes up.
SHIPS = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2
}

# Board size (10x10 grid)
BOARD_SIZE = 10

class Board:
    """
    Represents one player's board in Battleship
    The board keeps track of where ships are placed and which cells have been shot at.
    It also tells the caller whether a shot is a hit, miss, or sunk.
    """
    def __init__(self):
        # 2D grid: None means empty, ship name means a ship is there.
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Keep track of every shot that has been fired
        # Each entry is (row, col) -> "hit" or "miss".
        self.shots = {}

        # For each ship, store the list of (row, col) cells it sits on.
        # Example: {"Carrier": [(0,0), (0,1), (0,2), (0,3), (0,4)]}
        self.ship_positions = {}

        # Track how many cells of each ship have been hit.
        # When hits equal the ship's size, the ship is sunk.
        self.ship_hits = {}

        # Automatically place all ships randomly when the board is created.
        self._place_all_ships()

    # Ship placement
    def _place_all_ships(self):
        """
        Place every ship on the board in a random valid spot.
        """
        for ship_name, ship_size in SHIPS.items():
            self._place_single_ship(ship_name, ship_size)

    def _place_single_ship(self, ship_name, ship_size):
        """
        Keep trying random positions and directions until the ship fits on the board without overlapping another ship.
        """
        placed = False

        while not placed:
            # Pick a random direction: 0 = horizontal, 1 = vertical.
            direction = random.randint(0, 1)

            if direction == 0:
                # Horizontal: ship goes left to right.
                row = random.randint(0, BOARD_SIZE - 1)
                col = random.randint(0, BOARD_SIZE - ship_size)
                cells = [(row, col + i) for i in range(ship_size)]
            else:
                # Vertical: ship goes top to bottom.
                row = random.randint(0, BOARD_SIZE - ship_size)
                col = random.randint(0, BOARD_SIZE - 1)
                cells = [(row + i, col) for i in range(ship_size)]

            # Make sure none of those cells already have a ship.
            if all(self.grid[r][c] is None for r, c, in cells):
                # Place the ship on the grid.
                for r, c in cells:
                    self.grid[r][c] = ship_name
                
                # Save the positions and set hit count to zero.
                self.ship_positions[ship_name] = cells
                self.ship_hits[ship_name] = 0
                placed = True
    
    # Shooting logic
    def take_shot(self, row, col):
        """
        Fire a shot at the given (row, col).
        Returns one of three strings:
            "hit" - a ship was hit but not sunk yet
            "miss" - no ship at that cell
            "sunk" - a ship was hit and all its cells are not hit
        Returns None if the cell was already shot at (invalid move).
        """
        # Don't allow shooting the same cell twice.
        if (row, col) in self.shots:
            return None

        # Check what is on that cell.
        ship_name = self.grid[row][col]

        if ship_name is None:
            # Nothing there - it's a miss.
            self.shots[(row, col)] = "miss"
            return "miss"
        else:
            # A ship is there - it's a hit.
            self.shots[(row, col)] = "hit"
            self.ship_hits[ship_name] += 1

            # Check if every cell of this ship has been hit.
            if self.ship_hits[ship_name] == SHIPS[ship_name]:
                return "sunk"
            return "hit"
        
    # Helper functions
    def all_ships_sunk(self):
        """
        Return True if every ship on this board has been sunk.
        """
        for ship_name in SHIPS:
            if self.ship_hits[ship_name] < SHIPS[ship_name]:
                return False
        return True
    
    def is_valid_shot(self, row, col):
        """
        Check if a shot is inside the grid and hasn't been tried yet.
        """
        if row < 0 or row >= BOARD_SIZE:
            return False
        if col < 0 or col >= BOARD_SIZE:
            return False
        if (row, col) in self.shots:
            return False
        return True
    
    def get_sunk_ships(self):
        """
        Return a list of ship names that have been fully sunk.
        """
        sunk = []
        for ship_name in SHIPS:
            if self.ship_hits[ship_name] == SHIPS[ship_name]:
                sunk.append(ship_name)
        return sunk
    
    def get_remaining_ships(self):
        """
        Return a list of ship names that are still alive.
        """
        alive = []
        for ship_name in SHIPS:
            if self.ship_hits[ship_name] < SHIPS[ship_name]:
                alive.append(ship_name)
        return alive
    
    def display(self, show_ships=False):
        """
        Print the board to the terminal
        If show_ships is True, unhit ship cells show as 'S'.
        Otherwise, only hits and misses are shown (opponent's view).
        Symbols:
            . = unknown / empty
            S = ship (only when show_ships is True)
            X = hit
            O = miss
        """
        # Column headers.
        header = " " + " ".join(str(i) for i in range(BOARD_SIZE))
        print(header)

        for row in range(BOARD_SIZE):
            # Row label (A-J).
            label = chr(ord('A') + row)
            row_str = label + " "

            for col in range(BOARD_SIZE):
                if (row, col) in self.shots:
                    if self.shots[(row, col)] == "hit":
                        row_str += "X "
                    else:
                        row_str += "0 "
                elif show_ships and self.grid[row][col] is not None:
                    row_str += "S "
                else:
                    row_str += ". "

            print(row_str.rstrip())