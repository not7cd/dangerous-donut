from abc import *
import numpy as np

GRID_DIRECTIONS = [[1, 0], [0, 1], [-1, 0], [0, -1]]
ODDR_DIRECTIONS = [
    np.array([[+1, 0], [0, -1], [-1, -1], [-1, 0], [-1, +1], [0, +1]]),
    np.array([[+1, 0], [+1, -1], [0, -1], [-1, 0], [0, +1], [+1, +1]]),
]


class Coordinate(ABC):
    """docstring for Coordinate"""

    @abstractmethod
    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    @abstractmethod
    def directions(self):
        """
        :return: list of all possible directions
        """
        pass

    @property
    @abstractmethod
    def neighbours(self):
        """
        :return: coordinates in neghbourhood of self
        """
        pass

    def __repr__(self):
        return str([self.x, self.y])

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


class GridCoordinate(Coordinate):
    directions = np.array(GRID_DIRECTIONS)

    def __init__(self, x=0, y=0):
        super(GridCoordinate, self).__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        return str([self.x, self.y])

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    @property
    def neighbours(self):
        possible = np.array([self.x, self.y]) + self.directions
        return [GridCoordinate(x, y) for x, y in possible]


class HexCoordinate(Coordinate):
    def __init__(self, x=0, y=0):
        super(HexCoordinate, self).__init__()
        self.x = x
        self.y = y

    @property
    def directions(self):
        parity = self.y & 1
        return ODDR_DIRECTIONS[parity]

    @property
    def neighbours(self):
        possible = np.array([self.x, self.y]) + self.directions
        return [HexCoordinate(x, y) for x, y in possible]
