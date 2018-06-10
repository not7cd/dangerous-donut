from abc import *
import logging
import random

from simulation.errors import OccupiedFieldException

logger = logging.getLogger(__name__)


class Action(ABC):
    """Abstract method for Organism action"""

    def __init__(self, caller):
        self.caller = caller

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.caller)

    @abstractmethod
    def execute(self, board):
        """
        executes action on board
        """
        logger.info("%r", self)


class DoNothing(Action):
    def execute(self, board):
        logger.info("%r", self)


class Move(Action):
    def execute(self, board):
        logger.info("%r", self)

        start_position = self.caller.position
        target_position = random.choice(start_position.neighbours)

        if board.is_occupied(target_position):
            target = board.get_by_coord(target_position)
            logger.debug("occupied by %r", target)
            fight = Fight(self.caller, target)
            logger.debug("%r starts fight with %r", self.caller, target)
            fight.execute(board)

        # is alive        
        if self.caller is not None:
            try:
                board.move(start_position, target_position)
            except OccupiedFieldException as e:
                logger.error("Still occupied!!!")
                board.remove(target_position)
                board.move(start_position, target_position)
                logger.error("Force moving")


class Fight(Action):
    def __init__(self, caller, target):
        self.caller = caller
        self.target = target

    def __repr__(self):
        return "{}({!r}, {!r})".format(
            self.__class__.__name__, self.caller, self.target
        )

    def execute(self, board):
        logger.info("%r", self)
        if self.caller.strength >= self.target.strength:
            logger.info("%r lost against attacker", self.target)
            self.target.alive = False
        else:
            logger.info("%r lost against defender", self.caller)
            self.caller.alive = False


class Spread(Action):
    def execute(self, board):
        if random.randint(0, 100) < self.caller.spread_chance:
            logger.info("%r", self)
            start = self.caller.position
            new_position = random.choice(start.neighbours)
            if not board.is_occupied(new_position):
                child = self.caller.__class__(new_position)
                board.place_org(child)


class SuperSpread(Spread):
    def execute(self, board):
        super(SuperSpread   , self).execute(board)
        super(SuperSpread, self).execute(board)
        super(SuperSpread, self).execute(board)
