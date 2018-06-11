import logging

from simulation.errors import OccupiedFieldException
from simulation.coordinate import GridCoordinate, HexCoordinate, Coordinate
import simulation.life as life

logger = logging.getLogger(__name__)


# TODO: inherit from dict
class Board:
    """
    Container for organisms
    """

    def __init__(self, dimensions, wraparound=False, mode="grid"):
        self.wraparound = wraparound
        self.dimensions = dimensions
        self.organisms = {}
        self.mode = mode

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
        new_coord = HexCoordinate(x, y) if self.mode == "grid" else GridCoordinate(x, y)

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

    def purge(self):
        """resets board"""
        logger.warning("Purging board")
        self.organisms = {}

    def by_initiative(self):
        """
        :return: 
        """
        return sorted(self.entities(), key=lambda org: (-org.initiative, -org.age))


class World:
    """docstring for World"""

    def __init__(self, dimensions, factory=None, mode="grid"):
        self.dimensions = dimensions
        self.factory = factory
        self.board = Board(dimensions, wraparound=True, mode=mode)
        self.turn_count = 0
        self.mode = mode

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
                    next_action = action.execute(self.board)

                    while next_action is not None:
                        next_action = next_action.execute(self.board)

                except Exception as e:
                    logger.error("%s during %r", e, action)
                    raise e
            else:
                logger.info("%r is dead, moving on", organism)

        # TODO wtf is this hack
        for organism in list(self.board.entities()):
            if not organism.alive:
                logger.warning(
                    "deleting %r", self.board.get_by_coord(organism.position)
                )
                self.board.remove(organism.position)

        logger.info(
            "End of turn %s, %s pops alive", self.turn_count, len(self.board.organisms)
        )

    def print_board(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                organism = list(
                    filter(
                        lambda o: o.position == GridCoordinate(x, y),
                        self.board.entities(),
                    )
                )
                if organism:
                    print("{}".format(organism[0]), end="")
                else:
                    print(" ", end="")
            print("")

    def generate(self):
        """
        Populates world with worlds factory, if doesnt exist will create own
        :return:
        """
        if self.board.organisms:
            self.board.purge()

        if self.factory is None:
            factory = self.factory = life.OrganismFactory(
                self.dimensions, mode=self.mode
            )
            factory.register(life.Grass, 5)
            factory.register(life.Dandelion, 1)
            factory.register(life.Wolf, 8)
            factory.register(life.Sheep, 10)
            factory.register(life.Belladonna, 3)
            factory.register(life.Guarana, 3)
        else:
            factory = self.factory

        for org in factory.generate_registered():
            try:
                self.board.place_org(org)
            except OccupiedFieldException:
                logger.error("Position occupied, won't generate %r", org)
