"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

# Global variables

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    # replace with your code
    # define variables and lists
    length = len(line)
    new_line = []
    final_line = []
    # step 1
    for ind in range(0, length):
        if line[ind] != 0:
            new_line.append(line[ind])
    n_zero1 = length - len(new_line)
    new = new_line + [0]*n_zero1
    # step 2
    for ind in range(0, length - 1):
        if new[ind] == new[ind + 1]:
            new[ind] = new[ind]*2
            new[ind + 1] = 0
    # step 3
    for ind in range(0, length):
        if new[ind] != 0:
            final_line.append(new[ind])
    n_zero2 = length - len(final_line)
    final = final_line + [0]*n_zero2
    #return []
    return final

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.height = grid_height
        self.width = grid_width
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self.GRID = [[0 + 0 for col in range(self.width)]
                            for row in range(self.height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        string = "["
        for row in range(self.height - 1):
            string += str(self.GRID[row]) + '\n '
        string += str(self.GRID[self.height - 1])
        string += "]"
        return string
    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        temp = []
        merge_bool = False
        INDEX = {UP: [(0, num) for num in range(self.width)],
                 DOWN: [(self.height - 1, num) for num in range(self.width)],
                 LEFT: [(num, 0) for num in range(self.height)],
                 RIGHT: [(num, self.width - 1) for num in range(self.height)]}
        for item in INDEX[direction]: 
            for step in range(min(self.height, self.width)):              
                row = item[0] + step * OFFSETS[direction][0]
                col = item[1] + step * OFFSETS[direction][1]
                temp.append(self.GRID[row][col]) 
                new = merge(temp)
            if new != temp:
                merge_bool = True
            ind = 0
            for num in new:
                row = item[0] + ind * OFFSETS[direction][0]
                col = item[1] + ind * OFFSETS[direction][1]
                self.GRID[row][col] = new[ind]
                ind += 1
            temp = []
        if merge_bool:
            self.new_tile()
            merge_bool = False            
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        row_rand = random.choice(range(self.height))
        col_rand = random.choice(range(self.width))
        
        while True:
            if self.GRID[row_rand][col_rand] == 0:
                if random.choice(range(10)) == 1:
                    self.GRID[row_rand][col_rand] = 4
                    break
                else:
                    self.GRID[row_rand][col_rand] = 2 
                    break
            else:
                row_rand = random.choice(range(self.height))
                col_rand = random.choice(range(self.width))

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self.GRID[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self.GRID[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
