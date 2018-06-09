import logging
from simulation.coordinate import GridCoordinate as Coord, Coordinate

logger = logging.getLogger(__name__)


class Board:
    """docstring for Board"""

    def __init__(self, dimensions, wraparound=False):
        self.wraparound = False
        self.dimensions = dimensions
        self.organisms = {}

    def get_by_coord(self, coord):
        org = self.organisms.get(coord, None)
        if org is not None:
            assert org.position == coord
        return org

    def put_on_coord(self, coord, org):
        if org is not None:
            assert org.position == coord

        logger.debug("Placing %r at %s", org, coord)
        self.organisms[coord] = org

    def place_org(self, org):
        self.put_on_coord(org.position, org)

    def entities(self):
        return self.organisms.values()

    def move(self, start, end):
        """
        moves objects from position to position
        :start: object position
        :end: where will object end up
        """
        assert isinstance(start, Coordinate)
        assert isinstance(end, Coordinate)

        obj = self.get_by_coord(start)
        obj.position = end
        self.put_on_coord(end, obj)
        del self.organisms[start]


class World:
    """docstring for World"""

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.board = Board(dimensions)
        self.turn_count = 0

    def turn(self):
        self.turn_count += 1
        logger.info("Turn %s", self.turn_count)
        queue = self._initiative()

        for organism in queue:
            organism.age += 1

        for organism in queue:
            action = organism.action()
            action.execute(self.board)

        logger.info("End of turn %s, %s pops alive", self.turn_count, len(self.board.organisms))

    def _initiative(self):
        return sorted(
            self.board.entities(), key=lambda org: (-org.initiative, -org.age)
        )

    def print_board(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                organism = list(
                    filter(lambda o: o.position == Coord(x, y), self.board.entities())
                )
                if organism:
                    print("{}".format(organism[0]), end="")
                else:
                    print(" ", end="")
            print("")
