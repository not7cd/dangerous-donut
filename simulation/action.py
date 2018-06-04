class Action(object):
    """docstring for ClassName"""
    def __init__(self):
        self.caller = None

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)

    def execute():
        print('did nothing')

class DoNothing(Action):
    pass

class Move(Action):
    pass

class Spread(Action):
    pass

class SuperSpread(Spread):
    def execute(self):
        super(SuperSpread, self).execute()
        super(SuperSpread, self).execute()
        super(SuperSpread, self).execute()