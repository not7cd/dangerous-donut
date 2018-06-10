from abc import *
import logging
import random
from simulation.action import *
from simulation.coordinate import GridCoordinate as Coord
from simulation.helpers import with_surrogates, color_from_string

# mappinf for ascii to emoji
ASCII_EMOJI = {
    "o": "🐛",
    "p": "🌱",
    "A": "🐾",
    "W": "🐺",
    "d": "🌼"
}

MODE = "ascii"

logger = logging.getLogger(__name__)


class Organism(ABC):
    """docstring for Organism"""
    @abstractmethod
    def __init__(self, position):
        self.position = position
        self.initiative = 0
        self.strength = 0

        self.age = 0
        self.alive = True

        self.ascii_repr = "o"
        self.color = color_from_string(self.__class__.__name__)

    def __repr__(self):
        return "{}({}, {}, {})".format(
            self.__class__.__name__, self.position, self.age, self.initiative
        )

    def __str__(self):
        return (
            with_surrogates(ASCII_EMOJI.get(self.ascii_repr, self.ascii_repr))
            if MODE == "emoji"
            else self.ascii_repr
        )

    @abstractmethod
    def action(self):
        return DoNothing(self)


class Plant(Organism, ABC):
    @abstractmethod
    def __init__(self, position):
        super(Plant, self).__init__(position)
        self.spread_chance = 33
        self.ascii_repr = "p"

    @abstractmethod
    def action(self):
        return Spread(self)


class Animal(Organism, ABC):
    @abstractmethod
    def __init__(self, position):
        super(Animal, self).__init__(position)
        self.ascii_repr = "A"

    @abstractmethod
    def action(self):
        return Move(self)


class Grass(Plant):
    def __init__(self, position):
        super(Grass, self).__init__(position)
        self.ascii_repr = ","
        self.spread_chance = 33

    def action(self):
        return super(Grass, self).action()


class Dandelion(Plant):
    def __init__(self, position):
        super(Dandelion, self).__init__(position)
        self.ascii_repr = "d"
        self.spread_chance = 33

    def action(self):
        return SuperSpread(self)


class Sheep(Animal):
    def __init__(self, position):
        super(Sheep, self).__init__(position)
        self.ascii_repr = "S"
        self.initiative = 4
        self.strength = 4

    def action(self):
        return super(Sheep, self).action()


class Wolf(Animal):
    def __init__(self, position):
        super(Wolf, self).__init__(position)
        self.ascii_repr = "W"
        self.initiative = 5
        self.strength = 9

    def action(self):
        return super(Wolf, self).action()


class OrganismFactory:
    """docstring for OrganismFactory"""

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.organisms = []

    def register(self, organism, qty):
        """
        register organism class to generate later
        :param organism:
        :param qty:
        :return:
        """
        self.organisms.append((organism, qty))

    def position_generator(self, number):
        for _ in range(number):
            yield self.random_position()

    def random_position(self):
        return Coord(*tuple(random.randrange(d) for d in self.dimensions)[:2])

    def generate(self, organism, qty):
        for _ in range(qty):
            yield organism(position=self.random_position())

    def generate_registered(self):
        for org, qty in self.organisms:
            for _ in range(qty):
                yield org(position=self.random_position())
