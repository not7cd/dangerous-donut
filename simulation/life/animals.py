from simulation.life.base import Animal


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


class Antelope(Animal):
    pass


class Fox(Animal):
    pass


class Turtle(Animal):
    pass


class CyberSheep(Animal):
    pass
