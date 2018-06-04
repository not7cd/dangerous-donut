class World():
    """docstring for World"""
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.organisms = []

    def turn(self):
        queue = self._initiative()

        for organism in queue:
            organism.age += 1

        for organism in queue:
            print('{}'.format(organism), organism.action())

    def _initiative(self):
        return sorted(self.organisms, key=lambda org: (-org.initiative, -org.age))

    def print_board(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                organism = list(filter(lambda o: o.position == (x, y), self.organisms))
                if organism:
                    print('{}'.format(organism[0]), end='')
                else:
                    print(' ', end='')
            print('')
