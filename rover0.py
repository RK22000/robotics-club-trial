from typing import Any
import pygame
from pygame import Vector2
import heapq
import proj_utils

class Rover:
    def __init__(self, grid, cell_size, start, end) -> None:
        self.grid = grid
        self.known_blocks = dict() # x -> set(y)
        self.cell_size = cell_size
        self.start = start if type(start) is pygame.Vector2 else pygame.Vector2(*start)
        self.end = end if type(end) is pygame.Vector2 else pygame.Vector2(*end)
        self.explored = dict() # x0 -> y0 -> set((x1,y1), (x2,y2), ...)
        self.pos = self.start
    
    def huristic_path(self) -> tuple[int,list[tuple[int, int]]]: # cost, path
        pos = self.pos
        blocks = self.known_blocks
        prev = dict()
        q = [(0, (pos.y, pos.x), None)] # cost, cord, prev_cord # look on x axis then on y axis

        while q:
            c, n, p = heapq.heappop(q)
            if n in prev: continue
            prev[n] = p
            if n==(self.end.y, self.end.x):
                break

            neighbors = [(n[0]+1, n[1]), (n[0], n[1]+1), (n[0]-1, n[1]), (n[0], n[1]-1)]
            neighbors = filter(lambda i:proj_utils.valid_cell(Vector2(i[1],i[0]), *self.grid[1], blocks), neighbors)
            for nei in neighbors:
                heapq.heappush(q, (c+1, nei, n))
            
        if n!=(self.end.y, self.end.x): return [None, []]
        path = [n]
        while prev[path[-1]]:
            path.append(prev[path[-1]])
        path = [(x, y) for y,x in path]
        return [c, path]






    def draw(self, screen: pygame.Surface) -> None:
        cell_size = self.cell_size
        for x in self.explored:
            for y in self.explored[x]:
                for p in self.explored[x][y]:
                    pygame.draw.line(screen, 'blue', Vector2(x+0.5, y+0.5)*cell_size, Vector2(p[0]+0.5, p[1]+0.5)*cell_size)
        _, hpath = self.huristic_path()
        if len(hpath) > 1:
            hpath = [Vector2(x+0.5, y+0.5)*cell_size for x, y in hpath]
            pygame.draw.lines(screen, 'green', False, hpath)
        pygame.draw.circle(screen, 'blue', self.pos*cell_size + pygame.Vector2(0.5*cell_size, 0.5*cell_size), 0.25*cell_size)
        pygame.draw.circle(screen, 'green', self.end*cell_size + pygame.Vector2(0.5*cell_size, 0.5*cell_size), 0.25*cell_size)

    
    
    def pick_next_cell(self):
        pos = self.pos
        pot_next = [(pos.x+1, pos.y), (pos.x, pos.y+1), (pos.x-1, pos.y), (pos.x, pos.y-1)]
        # pot_next2 = []
        # for x, y in pot_next:
        #     if not self.valid_cell(Vector2(x, y), self.grid[0]):
        #         self.known_blocks.setdefault(x, set()).add(y)
        #         continue
        #     pot_next2.append((x,y))
        # pot_next = [(c, (y, x)) for c in self.huristic_path(Vector2(x, y)) for x, y in pot_next2]
        # next = min(pot_next)

        blocked = [(x,y) for x,y in pot_next if not proj_utils.valid_cell(Vector2(x, y), *self.grid[1], self.grid[0])]
        for x,y in blocked:
            self.known_blocks.setdefault(x, set()).add(y)
        c, p = self.huristic_path()
        

        if not c:
            return None
        next = Vector2(p[-2][0], p[-2][1])
        # next = Vector2(self.pos.x+1, self.pos.y)
        # if not self.valid_cell(next, self.grid[0]): return
        return next

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        next = self.pick_next_cell()
        self.set_next_node(next) if next else None
    
    
    def set_next_node(self, next):
        self.explored.setdefault(self.pos.x, dict()).setdefault(self.pos.y, set()).add((next.x, next.y))
        self.pos = next
