from simulation.action import SuperSpread, KillNeighbours
from simulation.life.base import Plant


class Grass(Plant):
    def __init__(self, position):
        super(Grass, self).__init__(position)
        self.ascii_repr = ","

    def action(self):
        return super(Grass, self).action()


class Guarana(Plant):
    def __init__(self, position):
        super(Guarana, self).__init__(position)
        self.ascii_repr = "g"

    def action(self):
        return super(Guarana, self).action()


class Dandelion(Plant):
    def __init__(self, position):
        super(Dandelion, self).__init__(position)
        self.ascii_repr = "d"

    def action(self):
        return SuperSpread(self)


class Hogweed(Plant):
    def __init__(self, position):
        super(Hogweed, self).__init__(position)
        self.ascii_repr = "h"
        self.strength = 10

    def action(self):
        return KillNeighbours(self)


class Belladonna(Plant):
    def __init__(self, position):
        super(Belladonna, self).__init__(position)
        self.ascii_repr = "b"
        self.strength = 99

    def action(self):
        return super(Belladonna, self).action()
