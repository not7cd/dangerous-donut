import random
from simulation.action import DoNothing, Spread

class Organism():
    """docstring for Organism"""
    def __init__(self, position):
        self.age = 0
        self.initiative = 0
        self.position = position

    def __repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__, self.position, self.age, self.initiative)

    def __str__(self):
        return '🐛'

    def action(self):
        return DoNothing() 
        
class Plant(Organism):
    def __init__(self, position):
        super(Plant, self).__init__(position)
        self.spread_chance = 0

    def __str__(self):
        return '🌱'

    def action(self):
        return Spread()

class Animal(Organism):
    def __init__(self, position):
        super(Animal, self,).__init__(position)
        self.initiative = 1

    def __str__(self):
        return '🐾'

class Wolf(Animal):
    def __init__(self, position):
        super(Wolf, self).__init__(position)
        self.initiative = 5

    def __str__(self):
        return '🐺'


class OrganismFactory():
    """docstring for OrganismFactory"""
    def __init__(self, dimensions):
        self.dimensions = dimensions

    def position_generator(self, number):
        generated = set()

        for _ in range(number):
            yield self.random_position()

    def random_position(self):
        return tuple(random.randrange(d) for d in self.dimensions)

    def generate(self, organism, qty):
        for _ in range(qty):
            yield organism(position=self.random_position())
