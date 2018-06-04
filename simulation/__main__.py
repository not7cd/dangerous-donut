from simulation.world import World
from simulation.life import *

WORLD_DIMENSION = (20, 20)
TURNS = 20

if __name__ == '__main__':
    world = World(WORLD_DIMENSION)

    factory = OrganismFactory(WORLD_DIMENSION)

    world.organisms += list(factory.generate(Organism, 5))
    world.organisms += list(factory.generate(Plant, 5))
    world.organisms += list(factory.generate(Animal, 5))
    world.organisms += list(factory.generate(Wolf, 5))


    for _ in range(TURNS):
        world.turn()
        world.print_board()
