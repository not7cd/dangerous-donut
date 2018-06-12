from simulation.action import SuperSpread, KillNeighbours, Spread
from simulation.life import Plant


class Grass(Plant):
    def __init__(self, position):
        super(Grass, self).__init__(position)
        self.ascii_repr = ","

    def action(self):
        super(Grass, self).action()
        return Spread(self)


class Guarana(Plant):
    def __init__(self, position):
        super(Guarana, self).__init__(position)
        self.ascii_repr = "g"

    def action(self):
        super(Guarana, self).action()
        return Spread(self)


class Dandelion(Plant):
    def __init__(self, position):
        super(Dandelion, self).__init__(position)
        self.ascii_repr = "d"

    def action(self):
        super(Dandelion, self).action()
        return SuperSpread(self)


class Hogweed(Plant):
    def __init__(self, position):
        super(Hogweed, self).__init__(position)
        self.ascii_repr = "h"
        self.strength = 10

    def action(self):
        super(Hogweed, self).action()
        return KillNeighbours(self)


class Belladonna(Plant):
    def __init__(self, position):
        super(Belladonna, self).__init__(position)
        self.ascii_repr = "b"
        self.strength = 99

    def action(self):
        super(Belladonna, self).action()
        return Spread(self)
