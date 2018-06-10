from simulation import coordinate as co
from simulation import world, life
import numpy as np


def test_GridCoordinate():
    c = co.GridCoordinate(5, 5)

    assert len(c.directions) == 4
    assert np.array_equal(c.directions, np.array([[1, 0], [0, 1], [-1, 0], [0, -1]]))
    assert np.array_equal(
        [[cn.x, cn.y] for cn in c.neighbours],
        np.array([[6, 5], [5, 6], [4, 5], [5, 4]]),
    )

    del c.neighbours[0]

    assert len(c.neighbours) == 4


def test_Board():
    DIMENSIONS = (5, 5)
    board = world.Board(DIMENSIONS)
    org = life.Organism(co.GridCoordinate(0, 0))

    board.place_org(org)

    assert org is board.get_by_coord(co.GridCoordinate(0, 0))

    board.move(co.GridCoordinate(0, 0), co.GridCoordinate(1, 1))

    assert board.get_by_coord(co.GridCoordinate(1, 1)) is org
    assert board.get_by_coord(co.GridCoordinate(0, 0)) is None


def test_Board_is_occupied():
    DIMENSIONS = (5, 5)
    board = world.Board(DIMENSIONS)
    org = life.Organism(co.GridCoordinate(0, 0))

    board.place_org(org)

    assert board.is_occupied(co.GridCoordinate(0, 0)) is True
    assert board.is_occupied(co.GridCoordinate(1, 1)) is False
