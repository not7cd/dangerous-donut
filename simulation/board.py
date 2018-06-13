from collections import defaultdict


class Board:
    """
    Moves thing around, holds agents, and keeps their positions in place
    >>> b = Board()
    >>> a = Agent()
    >>> a.position = Position(1, 2)
    >>> b.add(a)
    >>> b[Position(1, 2)]
    Agent()

    """
    def __init__(self):
        self._agents = defaultdict()

    def add(self, agent):
        if agent.position in self._agents:
            raise ValueError("agent exists under {}".format(agent.position))

        self._agents[agent.position] = agent

    def remove(self, agent):
        if agent.position not in self._agents:
            raise KeyError("agent not on board")

        del self._agents[agent.position]

    def __getitem__(self, position):
        return self._agents[position]

    def __setitem__(self, position, agent):
        agent.position = position
        self._agents[position] = agent

    def __delitem__(self, position):
        if position not in self._agents:
            raise KeyError("agent not on board")
        del self._agents[position]

    def __contains__(self, position):
        return position in self._agents

    def __iter__(self):
        return (position for position in self._agents)

    def __len__(self):
        return len(self._agents)


class BoardManager:
    def __init__(self, dimensions):
        self._board = Board()
        self.dimensions = dimensions

    @property
    def size(self):
        return self.dimensions[0] * self.dimensions[1]

    @property
    def free_space(self):
        return self.size - len(self._board)

    def move(self, start, to):
        self._board[to] = self._board[start]
        del self._board[to]

