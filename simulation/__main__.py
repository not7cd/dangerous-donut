import logging

from simulation.world import World
from simulation.life import *

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

WORLD_DIMENSION = (20, 20)
TURNS = 5

if __name__ == "__main__":
    world = World(WORLD_DIMENSION)
    world.generate()

    for turn in range(TURNS):
        world.turn()
        world.print_board()
