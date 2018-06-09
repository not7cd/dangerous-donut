import logging

from simulation.world import World
from simulation.life import *

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

WORLD_DIMENSION = (20, 20)
TURNS = 3

if __name__ == "__main__":
    world = World(WORLD_DIMENSION)

    factory = OrganismFactory(WORLD_DIMENSION)

    for o in factory.generate(Plant, 5):
        world.board.place_org(o)

    for o in factory.generate(Animal, 5):
        world.board.place_org(o)

    for turn in range(TURNS):
        print("T: {}".format(turn))
        world.turn()
        world.print_board()
