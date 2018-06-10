from simulation.action import *
from simulation.coordinate import GridCoordinate as Coord
from simulation.helpers import with_surrogates

# mappinf for ascii to emoji
ASCII_EMOJI = {"o": "🐛", "p": "🌱", "A": "🐾", "W": "🐺", "d": "🌼"}

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

    # TODO: collision


class Plant(Organism, ABC):
    @abstractmethod
    def __init__(self, position):
        super(Plant, self).__init__(position)
        self.spread_chance = 25
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


class OrganismFactory:
    """docstring for OrganismFactory"""

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.organisms_qty = []

    def register(self, organism, qty):
        """
        register organism class to generate later
        :param organism:
        :param qty:
        :return:
        """
        self.organisms_qty.append((organism, qty))

    @property
    def organisms(self):
        return [org for org, qty in self.organisms_qty]

    def position_generator(self, number):
        for _ in range(number):
            yield self.random_position()

    def random_position(self):
        return Coord(*tuple(random.randrange(d) for d in self.dimensions)[:2])

    def generate(self, organism, qty):
        for _ in range(qty):
            yield organism(position=self.random_position())

    def generate_registered(self):
        for org, qty in self.organisms_qty:
            for _ in range(qty):
                yield org(position=self.random_position())
