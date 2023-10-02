import honeycomb
from math import pi


class Dirs:
    UP=0
    UP_LEFT=1
    DOWN_LEFT=2
    DOWN = 3
    DOWN_RIGHT = 4
    UP_RIGHT = 5

angle = {
    Dirs.UP:0.0,
    Dirs.UP_LEFT:pi/3,
    Dirs.DOWN_LEFT : 2*pi/3,
    Dirs.DOWN : 3*pi/3,
    Dirs.DOWN_RIGHT : 4*pi/3,
    Dirs.UP_RIGHT : 5*pi/3
}

next_cell = {
    Dirs.UP: (0,-2),
    Dirs.UP_LEFT: (1,-1),
    Dirs.DOWN_LEFT: (1,1),
    Dirs.DOWN: (0,2),
    Dirs.DOWN_RIGHT: (-1,1),
    Dirs.UP_RIGHT: (-1,-1)
}

class BeePrime:
    def __init__(self) -> None:
        self.type = "Bee Prime"
        self.refresh()
    def refresh(self):
        self.blocks = set()
        self.pos = honeycomb.start
        self.goals = honeycomb.goals.copy()
        self.explored = [self.pos]
        self.mentally_explored = []
        self.mentally_explored_total = 0
        self.planned = []
        self.dir = Dirs.UP_RIGHT
        self.status_failed = False
        # Move to next planned step > Compute following steps > Orient towards next step
