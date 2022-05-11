#  board.py
#  
#  Copyright 2022  <Shaif Salehin, Arianna Martinez, I'munique Hill>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#  Source: https://github.com/jakeoeding/connect-4
#  Modified by: Shaif Salehin

import numpy as np

class Board:
    def __init__(self, row_count, column_count):
        self.row_count = row_count
        self.column_count = column_count
        self.grid = np.zeros((row_count, column_count))

    def is_valid_location(self, column):
        # Check if last row in column is empty
        return self.grid[self.row_count - 1, column] == 0

    def get_next_open_row(self, column):
        # Return first instance where row is empty
        for row in range(self.row_count):
            if self.grid[row, column] == 0:
                return row

    def drop_piece(self, row, column, turn):
        # Fill the specified point with the current turn
        self.grid[row, column] = turn

    def has_four_in_a_row(self, turn):
        # Check horizontally
        for r in range(self.row_count):
            for c in range(self.column_count - 3):
                if self.grid[r, c] == turn and self.grid[r, c + 1] == turn and self.grid[r, c + 2] == turn and self.grid[r, c + 3] == turn:
                    return True

        # Check vertically
        for r in range(self.row_count - 3):
            for c in range(self.column_count):
                if self.grid[r, c] == turn and self.grid[r + 1, c] == turn and self.grid[r + 2, c] == turn and self.grid[r + 3, c] == turn:
                    return True

        # Check diagonally upward
        for r in range(self.row_count - 3):
            for c in range(self.column_count - 3):
                if self.grid[r, c] == turn and self.grid[r + 1, c + 1] == turn and self.grid[r + 2, c + 2] == turn and self.grid[r + 3, c + 3] == turn:
                    return True

        # Check diagonally downward
        for r in range(3, self.row_count):
            for c in range(self.column_count - 3):
                if self.grid[r, c] == turn and self.grid[r - 1, c + 1] == turn and self.grid[r - 2, c + 2] == turn and self.grid[r - 3, c + 3] == turn:
                    return True

        return False

    def is_full(self):
        # Determine if every spot in the grid is filled
        return self.grid.all()

    def reset(self):
        # Fill the grid with zeros for a new round
        self.grid = np.zeros((self.row_count, self.column_count))

    def print_grid(self):
        # Display the game's state in the console
        print(np.flip(self.grid, 0))
