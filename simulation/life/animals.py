from simulation.life import Animal
from simulation.action import Move


class Sheep(Animal):
    def __init__(self, position):
        super(Sheep, self).__init__(position)
        self.ascii_repr = "S"
        self.initiative = 4
        self.strength = 4

    def action(self):
        super(Sheep, self).action()
        return Move(self)


class Wolf(Animal):
    def __init__(self, position):
        super(Wolf, self).__init__(position)
        self.ascii_repr = "W"
        self.initiative = 5
        self.strength = 9

    def action(self):
        super(Wolf, self).action()
        return Move(self)


class Antelope(Animal):
    pass


class Fox(Animal):
    pass


class Turtle(Animal):
    pass


class CyberSheep(Animal):
    def __init__(self, position):
        super(CyberSheep, self).__init__(position)
        self.ascii_repr = "§"
        self.initiative = 4
        self.strength = 11

    def action(self):
        super(CyberSheep, self).action()
        return Move(self)
