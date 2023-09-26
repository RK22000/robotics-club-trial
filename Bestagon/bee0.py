import honeycomb
from math import pi
from heapq import heappush, heappop

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

class Bee:
    def __init__(self) -> None:
        self.refresh()
    def refresh(self):
        self.blocks = set()
        self.pos = honeycomb.start
        self.goals = honeycomb.goals.copy()
        self.goal = list(self.goals)[0]
        self.explored = [self.pos]
        self.mentally_explored = []
        self.planned = []
        self.dir = Dirs.UP_RIGHT
        # Move to next planned step > Compute following steps > Orient towards next step
    def draw_bee(self):
        honeycomb.draw_bee(self.pos, angle[self.dir], 'orange')
    def draw(self):
        if len(self.explored) >=2:
            honeycomb.draw_path(self.explored, 'orange')
        if len(self.planned) >=2:
            honeycomb.draw_path(self.planned, 'green')
        self.draw_bee()
    def plan_path(self):
        # cost, cur, prev
        if self.pos in self.goals:
            self.goals.remove(self.pos)
        q = [(0, self.pos, None)]
        p = dict()
        while q:
            cost, cur, prev = heappop(q)
            if cur in p: continue
            p[cur]=prev
            if cur in self.goals:
                break
            for n in honeycomb.neighbours(cur):
                heappush(q, (cost+1, n, cur))
        if cur not in self.goals:
            self.planned=[]
            return
        self.planned = [cur]
        while self.planned[-1] in p:
            self.planned.append(p[self.planned[-1]])
        if self.planned[-1] is None:
            self.planned.pop()
            self.planned.pop()
        

            

        pass
    def step(self):
        self.plan_path()
        if not self.planned:
            return
        next = self.planned[-1]
        try:
            after = self.planned[-2]
            while (next[0]+next_cell[self.dir][0], next[1]+next_cell[self.dir][1])!=after:
                self.dir+=1
                if self.dir >= 6:
                    self.dir=0
        except IndexError:
            pass
        self.pos = next
        self.explored.append(next)