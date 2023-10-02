import honeycomb
from math import pi
from heapq import heappush, heappop
from bee import *

class Bee(BeePrime):
    def __init__(self, name='Dijkstra\'s Bee', heuristic=lambda a,b: 0) -> None:
        self.type = name
        self.name = name
        self.heuristic=heuristic
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
    def draw_bee(self):
        honeycomb.draw_bee(self.pos, angle[self.dir], 'orange' if not self.status_failed else 'red')
    def draw(self, epath='blue'):
        for cell in self.mentally_explored:
            honeycomb.draw_cell(cell, (0,255,0,150))
        if len(self.explored) >=2:
            honeycomb.draw_path(self.explored, epath)
        if len(self.planned) >=2:
            honeycomb.draw_path(self.planned, 'green')
        self.draw_bee()
    def plan_path(self, blocks=None):
        self.mentally_explored_total += len(self.mentally_explored)
        self.mentally_explored.clear()
        if self.pos in self.goals:
            self.goals.remove(self.pos)
        if not self.goals: # return if there are know goals
            self.planned.clear()
            return
        if blocks is None: blocks=self.blocks
        # cost, arrival cost, cur, prev
        q = [(0, 0, self.pos, None)]
        p = dict()
        while q:
            cost, arcost, cur, prev = heappop(q)
            if cur in p: continue
            p[cur]=prev
            self.mentally_explored.append(cur)
            if cur in self.goals:
                break
            for n in filter(lambda cell: cell not in blocks, honeycomb.neighbours(cur)):
                gc = [i for i in self.goals]
                gc = [self.heuristic(n, i) for i in gc]
                hc = min(gc)
                heappush(q, (arcost+1+hc, arcost+1, n, cur))
        if cur not in self.goals:
            self.planned=[]
            self.status_failed = True
            return
        self.planned = [cur]
        while self.planned[-1] in p:
            self.planned.append(p[self.planned[-1]])
        if self.planned[-1] is None:
            self.planned.pop()
            self.planned.pop()

    def step(self):
        self.plan_path()
        if not self.planned:
            return
        next = self.planned[-1]
        if next in honeycomb.blocks:
            self.blocks.add(next)
            return
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