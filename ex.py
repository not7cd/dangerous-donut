class Organism():
    """docstring for Organism"""
    alive = False

    def __init__(self):
        self.age = 0

    def __str__(self):
        return "..."

    @classmethod
    def generate(cls, number):
        return [cls() for n in range(number)]


class Plant(Organism):
    """docstring for Plant"""
    def __init__(self):
        super(Organism, self)
        self.alive = True

    def __str__(self):
        return "woosh"


class Animal(Organism):
    """docstring for Animal"""
    def __init__(self, arg):
        super(Animal, self).__init__()
        self.alive = True
        self.arg = arg
        
    def __str__(self):
        return "{}".format(self.arg)
        
    @classmethod
    def generate(cls, number):
        return [cls('xd') for n in range(number)]


if __name__ == '__main__':
    
    print(Organism.alive, Plant.alive)

    pool = Organism.generate(5)
    pool += Plant.generate(2)
    pool += Animal.generate(2)
    
    for a in pool:
        print('{} {}\n'.format(a.alive, a))
    print(Organism.alive, Plant.alive)