from abc import *
import logging
import random
from simulation.action import *
from simulation.coordinate import GridCoordinate as Coord
from simulation.helpers import with_surrogates, color_from_string

EMOJI = "🐛🌱🐾🐺🌼"
ASCII = "OPAWS"

MODE = "ascii"

logger = logging.getLogger(__name__)


class Organism(ABC):
    """docstring for Organism"""

    def __init__(self, position):
        self.age = 0
        self.initiative = 0
        self.position = position
        self.strength = 0
        self.alive = True

        self.repr_id = 0
        self.color = color_from_string(self.__class__.__name__)

    def __repr__(self):
        return "{}({}, {}, {})".format(
            self.__class__.__name__, self.position, self.age, self.initiative
        )

    def __str__(self):
        return with_surrogates(EMOJI[self.repr_id]) if MODE == "emoji" else ASCII[self.repr_id]

    @abstractmethod
    def action(self):
        return DoNothing(self)
    


class Plant(Organism):
    def __init__(self, position):
        super(Plant, self).__init__(position)
        self.spread_chance = 33
        self.repr_id = 1

    def action(self):
        return Spread(self)


class Animal(Organism):
    def __init__(self, position):
        super(Animal, self).__init__(position)
        self.initiative = 1
        self.repr_id = 2
        self.strength = 5

    def action(self):
        return Move(self)


class Wolf(Animal):
    def __init__(self, position):
        super(Wolf, self).__init__(position)
        self.initiative = 5
        self.repr_id = 3


class Dandelion(Plant):
    def __init__(self, position):
        super(Dandelion, self).__init__(position)
        self.spread_chance = 33
        self.repr_id = 4

    def action(self):
        # TODO: jakiś bug
        return SuperSpread(self)


class OrganismFactory:
    """docstring for OrganismFactory"""

    def __init__(self, dimensions):
        self.dimensions = dimensions

    def position_generator(self, number):
        generated = set()

        for _ in range(number):
            yield self.random_position()

    def random_position(self):
        return Coord(*tuple(random.randrange(d) for d in self.dimensions)[:2])

    def generate(self, organism, qty):
        for _ in range(qty):
            yield organism(position=self.random_position())
