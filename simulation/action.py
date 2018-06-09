import logging
import random

logger = logging.getLogger(__name__)

class Action(object):
    """docstring for ClassName"""

    def __init__(self, caller):
        self.caller = caller

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def execute(self, board):
        logger.info("%r -> %r", self.caller, self)


class DoNothing(Action):
    def execute(self, board):
        logger.info("%r -> %r", self.caller, self)


class Move(Action):
    def execute(self, board):
        logger.info("%r -> %r", self.caller, self)

        start = self.caller.position
        end = random.choice(start.neighbours)
        board.move(start, end)


class Spread(Action):
    def execute(self, board):
        if random.randint(0,100) < self.caller.spread_chance:
            logger.info("%r -> %r", self.caller, self)
            start = self.caller.position
            position = random.choice(start.neighbours)
            child = self.caller.__class__(position)

            board.place_org(child)


class SuperSpread(Spread):
    def execute(self, board):
        super(SuperSpread, self).execute(board)
        super(SuperSpread, self).execute(board)
        super(SuperSpread, self).execute(board)
