from abc import *
import numpy as np

GRID_DIRECTIONS = [[1, 0], [0, 1], [-1, 0], [0, -1]]


class Coordinate(ABC):
    """docstring for Coordinate"""

    @abstractmethod
    def __init__(self):
        pass

    @property
    def directions():
        """
        :return: list of all possible directions
        """
        pass

    @abstractmethod
    def neighbours(self):
        """
        :return: coordinates in neghbourhood of self
        """
        pass


class GridCoordinate(Coordinate):
    directions = np.array(GRID_DIRECTIONS)

    def __init__(self, x=0, y=0):
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
