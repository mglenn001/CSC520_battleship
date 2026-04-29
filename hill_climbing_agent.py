# Agent 2, local search with hill climbing.
# Shoots randomly until a hit, then searches neighbors and follows the ship's direction until it's sunk.

import random
from board import BOARD_SIZE

class HillClimbingAgent:
    """
    A smarter agent that uses hill climbing after getting a hit.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        """
        Clear everything for a new game.
        """
        self.available_shots = set()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.available_shots.add((row,col))

        # Hits from the current hunt (the ship we are chasing right now).
        # When that ship sinks, we clear this list.
        self.target_hits = []

        # Hits that aren't part of the current hunt.
        # This can happen if we accidentally hit a second ship
        # while chasing the first one.
        self.other_hits = []

        # The direction we are currently following after a hit.
        # None means we haven't picked a direction yet.
        self.current_direction = None

        # The four possible directions: up, down, left, right.
        self.directions = [(-1,0), (1,0), (0,-1), (0,1)]

        # Directions we already tried from the first hit.
        self.tried_directions = []

        # The first hit that started the current hunt.
        self.first_hit = None

    def choose_shot(self,board):
        """
        Pick the next cell to shoot.
        """
        # If we have a direction, keep following it.
        if self.first_hit and self.current_direction is not None:
            shot = self._follow_direction(board)
            if shot is not None:
                self.available_shots.discard(shot)
                return shot
            
        # If we have a first hit but no direction, try neighbors.
        if self.first_hit:
            shot = self._try_neighbor(board)
            if shot is not None:
                self.available_shots.discard(shot)
                return shot
            
        # No target - shoot randomly.
        shot = random.choice(list(self.available_shots))
        self.available_shots.discard(shot)
        return shot
    
    def _follow_direction(self,board):
        """
        Keep moving in the current direction from the last hit.
        """
        # Step forward from the most recent target hit.
        last_hit = self.target_hits[-1]
        dr, dc = self.current_direction
        next_row = last_hit[0] + dr
        next_col = last_hit[1] + dc

        # Check if this cell is valid.
        if board.is_valid_shot(next_row,next_col):
            return (next_row,next_col)
        
        # Can't go further - try the opposite direction from the first hit.
        opposite = (-dr,-dc)
        if opposite not in self.tried_directions:
            self.tried_directions.append(opposite)
            self.current_direction = opposite

            # Step from the frist hit in the opposite direction.
            next_row = self.first_hit[0] + opposite[0]
            nect_col = self.first_hit[1] + opposite[1]

            if board.is_valid_shot(next_row,next_col):
                return (next_row,nect_col)
            
        # Both directions exhausted - give up this direction.
        self.current_direction = None
        return None
    
    def _try_neighbor(self,board):
        """
        Try each untried direction from the first hit.
        """
        for direction in self.directions:
            if direction not in self.tried_directions:
                self.tried_directions.append(direction)
                dr, dc = direction
                next_row = self.first_hit[0] + dr
                next_col = self.first_hit[1] + dc

                if board.is_valid_shot(next_row,next_col):
                    # Set this as our direction in case it's a hit.
                    self.current_direction = direction
                    return (next_row,next_col)
        
        # All four directions tried.
        return None
    
    def update(self,row,col,result,sunk_ship):
        """
        Learn from the shot result and update our strategy.
        """
        if result == "hit":
            if self.first_hit is None:
                # Brand new target - start a hunt.
                self.first_hit = (row,col)
                self.target_hits = [(row,col)]
            else:
                # We are already hunting. Add is target hits.
                self.target_hits.append((row,col))
        elif result == "miss":
            if self.current_direction is not None:
                # We were following a direction and it missed.
                # Try the opposite direction from the first hit.
                dr, dc = self.current_direction
                opposite = (-dr,-dc)

                if opposite not in self.tried_directions:
                    self.tried_directions.append(opposite)
                    self.current_direction = opposite
                else:
                    # Already tried opposite - clear direction.
                    self.current_direction = None
        elif result == "sunk":
            # The ship we were chasing is sunk.
            # Add the final hit to target hits.
            self.target_hits.append((row,col))

            # Clean up and start chasing any leftover hits.
            self._handle_sunk()

    def _handle_sunk(self):
        """
        After a ship sinks, clean up and decide what to do next.
        """
        # Move any stray hits that might belong to other ships.
        # Stray hits are ones that don't line up with our direction.
        stray_hits = []

        if self.current_direction is not None and len(self.target_hits) > 1:
            dr, dc = self.current_direction
            for hit in self.target_hits:
                # Check if this hit is on the same line as the first hit.
                row_diff = hit[0] - self.first_hit[0]
                col_diff = hit[1] - self.first_hit[1]

                # It's on the same line if one axis matches and the
                # other axis moves in the right direction.
                on_line = False
                if dr == 0 and row_diff == 0:
                    # Horizontal line
                    on_line = True
                elif dc == 0 and col_diff == 0:
                    # Vertical line
                    on_line = True
                
                if not on_line:
                    stray_hits.append(hit)

        # Add any stray hits to the other_hits list.
        self.other_hits.extend(stray_hits)

        # Reset the hunt.
        self._reset_hunt()

        # If there are leftover hits, start chasing one of them.
        if self.other_hits:
            next_hit = self.other_hits.pop(0)
            self.first_hit = next_hit
            self.target_hits = [next_hit]

    def _reset_hunt(self):
        """
        Reset the hunting state so we go back to exploring.
        """
        self.current_direction = None
        self.tried_directions = []
        self.first_hit = None
        self.target_hits = []