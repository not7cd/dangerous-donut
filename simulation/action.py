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
        # logger.info("%r", self)
        pass


class Move(Action):
    def __init__(self, caller):
        super(Move, self).__init__(caller)
        self.start_position = self.caller.position
        self.target_position = random.choice(self.start_position.neighbours)

    def execute(self, board):
        logger.info("%r", self)

        if board.is_occupied(self.target_position):
            target = board.get_by_coord(self.target_position)
            if target.alive:
                logger.debug("occupied by %r", target)

                if type(self.caller) == type(target):
                    return Breed(self.caller)
                else:
                    return Fight(self.caller, target)

        try:
            board.move(self.start_position, self.target_position)
        except OccupiedFieldException as e:
            logger.warning("Still occupied!!! force move")
            board.remove(self.target_position)
            board.move(self.start_position, self.target_position)

        return DoNothing(self.caller)


class MoveTo(Move):
    def __init__(self, caller, target_position):
        super(MoveTo, self).__init__(caller)
        self.target_position = target_position


class Breed(Action):
    def __init__(self, caller):
        super(Breed, self).__init__(caller)
        self.target_position = random.choice(self.caller.position.neighbours)

    def execute(self, board):
        logger.info("%r", self)

        cls = type(self.caller)
        try:
            board.place_org(cls(self.target_position))
        except OccupiedFieldException:
            pass

        return DoNothing(self.caller)


class Fight(Action):
    def __init__(self, caller, target):
        super(Fight, self).__init__(caller)
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

            return MoveTo(self.caller, self.target.position)
        else:
            logger.info("%r lost against defender", self.caller)
            self.caller.alive = False
            return DoNothing(self.caller)


class Spread(Action):
    def execute(self, board):
        if random.randint(0, 100) < self.caller.spread_chance:
            logger.info("%r", self)
            start = self.caller.position
            new_position = random.choice(start.neighbours)
            if not board.is_occupied(new_position):
                child = self.caller.__class__(new_position)
                board.place_org(child)
        return DoNothing(self.caller)


class SuperSpread(Spread):
    def execute(self, board):
        super(SuperSpread, self).execute(board)
        super(SuperSpread, self).execute(board)
        super(SuperSpread, self).execute(board)
        return DoNothing(self.caller)
