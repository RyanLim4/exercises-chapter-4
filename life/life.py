"""Implements Conway's game of life."""

import numpy as np
from matplotlib import pyplot
from scipy.signal import convolve2d

glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])

blinker = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])

glider_gun = np.array([
    [0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0]
])


class Game:
    """Interface for Conway's game of life."""

    def __init__(self, size):
        """Construct a game with a board."""
        self.board = np.zeros((size, size))

    def play(self):
        """Start the game."""
        print("Playing life. Press ctrl + c to stop.")
        pyplot.ion()
        while True:
            self.move()
            self.show()
            pyplot.pause(0.0000005)

    def move(self):
        """Move the game."""
        stencil = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        neighbour_count = convolve2d(self.board, stencil, mode='same')

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                self.board[i, j] = 1 if (neighbour_count[i, j] == 3
                                         or (neighbour_count[i, j] == 2
                                         and self.board[i, j])) else 0

    def __setitem__(self, key, value):
        """Set indexing."""
        self.board[key] = value

    def show(self):
        """Display the board."""
        pyplot.clf()
        pyplot.matshow(self.board, fignum=0, cmap='binary')
        pyplot.show()

    def insert(self, pattern, coords):
        """Insert pattern at coords."""
        width, height = pattern.grid.shape
        x, y = coords
        self[x - width//2:x + width//2 + 1,
             y - height//2:y + height//2 + 1] = pattern.grid


class Pattern:
    """Array of cells which form a pattern."""

    def __init__(self, pattern):
        """Construct a pattern."""
        self.grid = pattern

    def flip_vertical(self):
        """Return pattern whose columns are reversed."""
        vert_flipped = np.array([col[::-1] for col in self.grid.T]).T
        return Pattern(vert_flipped)

    def flip_horizontal(self):
        """Return pattern whose rows are reversed."""
        horizontal_flipped = np.array([row[::-1] for row in self.grid])
        return Pattern(horizontal_flipped)

    def flip_diag(self):
        """Return transpose of inputted pattern."""
        return Pattern(self.grid.T)

    def rotate(self, n):
        """Return pattern after n right anticlockwise rotations."""
        if (n % 4 == 0):
            return self
        elif (n % 4 == 1):
            return self.flip_diag().flip_vertical()
        elif (n % 4 == 2):
            return self.flip_vertical().flip_horizontal()
        else:
            return self.flip_diag().flip_horizontal()
