import random


class PositionMeta:
    def __hash__(self):
        pass


class Position(PositionMeta):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class PositionAxial(PositionMeta):
    def __init__(self, r=0, q=0):
        self.r = r
        self.q = q


class PositionFactory:
    """Given Position class, will generate all """
    def __init__(self, cls):
        self._cls = cls
        self._cls_fields = cls._fields

    def random(self, bounds):
        args = zip(self._cls_fields, bounds)
        result = {field: random.randrange(bound) for field, bound in args}
        return self._cls(**result)

