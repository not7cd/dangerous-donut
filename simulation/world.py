import logging

from simulation.errors import OccupiedFieldException
from simulation.coordinate import GridCoordinate as Coord, Coordinate
from simulation.life import *

logger = logging.getLogger(__name__)


# TODO: inherit from dict
class Board:
    """
    Container for organisms
    """

    def __init__(self, dimensions, wraparound=False):
        self.wraparound = wraparound
        self.dimensions = dimensions
        self.organisms = {}

    @staticmethod
    def _handle_dimension_warparound(x, dimension):
        if x < 0:
            return x + dimension
        elif x >= dimension:
            return x - dimension
        else:
            return x

    def handle_warparound(self, coord):
        """
        :coord: any coordinate
        :return: coordinate in bounds wraped around
        """
        x = self._handle_dimension_warparound(coord.x, self.dimensions[0])
        y = self._handle_dimension_warparound(coord.y, self.dimensions[1])
        new_coord = Coord(x, y)

        if coord != new_coord:
            logger.debug("wraparound %r -> %r", coord, new_coord)
        return new_coord

    def get_by_coord(self, coord):
        if self.wraparound:
            coord = self.handle_warparound(coord)

        org = self.organisms.get(coord, None)
        if org is None:
            return None
        else:
            if org.position != coord:
                logger.error("%r %s", org, coord)
                raise Exception("%r %s", org, coord)
            return org

    def put_on_coord(self, coord, org):
        """
        Just put, can overwrite position
        """
        if self.wraparound:
            coord = self.handle_warparound(coord)

        logger.debug("Placing %r at %s", org, coord)
        org.position = coord
        self.organisms[coord] = org

    def place_org(self, org):
        """
        Will place on board if not occupied
        :param: organism with position
        """
        if self.is_occupied(org.position):
            logger.error("occupied by %r", self.get_by_coord(org.position))
            raise OccupiedFieldException

        self.put_on_coord(org.position, org)

    def entities(self):
        return self.organisms.values()

    def is_occupied(self, coord):
        if self.wraparound:
            coord = self.handle_warparound(coord)

        return self.get_by_coord(coord) is not None

    def move(self, start, end):
        """
        moves objects from position to position only if field is empty
        :start: object position
        :end: where will object end up
        """
        assert isinstance(start, Coordinate)
        assert isinstance(end, Coordinate)
        if self.is_occupied(end):
            logger.error("occupied by %r", self.get_by_coord(end))
            raise OccupiedFieldException

        obj = self.get_by_coord(start)
        obj.position = end

        self.put_on_coord(end, obj)
        del self.organisms[start]

    def remove(self, coord):
        if self.is_occupied(coord):
            if self.wraparound:
                coord = self.handle_warparound(coord)
            del self.organisms[coord]

    def by_initiative(self):
        """
        :return: 
        """
        return sorted(self.entities(), key=lambda org: (-org.initiative, -org.age))


class World:
    """docstring for World"""

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.board = Board(dimensions, wraparound=True)
        self.turn_count = 0

    def turn(self):
        self.turn_count += 1
        logger.info("Turn %s", self.turn_count)
        queue = self.board.by_initiative()

        for organism in queue:
            organism.age += 1

        for organism in queue:
            if organism.alive:
                action = organism.action()
                try:
                    action.execute(self.board)
                except Exception as e:
                    logger.error("%s during %r", e, action)
                    raise e
            else:
                logger.info("%r is dead, moving on", organism)

        # TODO this hack
        for organism in self.board.entities():
            if not organism.alive:
                logger.debug("deleting %r", self.board.get_by_coord(organism.position))
                self.board.remove(organism.position)

        logger.info(
            "End of turn %s, %s pops alive", self.turn_count, len(self.board.organisms)
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

    def generate(self):
        factory = OrganismFactory(self.dimensions)
        factory.register(Grass, 5)
        factory.register(Dandelion, 1)
        factory.register(Wolf, 5)
        factory.register(Sheep, 5)

        for org in factory.generate_registered():
            try:
                self.board.place_org(org)
            except OccupiedFieldException:
                logger.error("Position occupied, won't generate %r", org)
