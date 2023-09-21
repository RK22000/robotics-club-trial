import pygame
from pygame import Vector2
from math import pi, sin, cos, sqrt
import proj_utils
import heapq
import random
class Rover:
    # Preference right, down|right, down, down|left, left, up|left, up, up|right
    RIGHT = 0.0
    DOWN_RIGHT = pi/4
    DOWN = 2*DOWN_RIGHT
    DOWN_LEFT = 3*DOWN_RIGHT
    LEFT = 4*DOWN_RIGHT
    TOP_LEFT = 5*DOWN_RIGHT
    TOP = 6*DOWN_RIGHT
    TOP_RIGHT = 7*DOWN_RIGHT
    dirs = {
        RIGHT,
        DOWN_RIGHT,
        DOWN,
        DOWN_LEFT,
        LEFT,
        TOP_LEFT,
        TOP,
        TOP_RIGHT
    }
    next_cell = {
        RIGHT: Vector2(1,0),
        DOWN_RIGHT: Vector2(1,1),
        DOWN: Vector2(0,1),
        DOWN_LEFT: Vector2(-1,1),
        LEFT: Vector2(-1,0),
        TOP_LEFT: Vector2(-1,-1),
        TOP: Vector2(0,-1),
        TOP_RIGHT: Vector2(1,-1),
    }
    next_dir = {
        RIGHT: DOWN_RIGHT,
        DOWN_RIGHT: DOWN,
        DOWN: DOWN_LEFT,
        DOWN_LEFT: LEFT,
        LEFT: TOP_LEFT,
        TOP_LEFT: TOP,
        TOP: TOP_RIGHT,
        TOP_RIGHT: RIGHT
    }
    heuristics = [
        lambda a, b: 0,
        lambda a, b: sqrt((b.x-a.x)**2+(b.y-a.y)**2)
    ]
    def __init__(self, parameters: proj_utils.Parameters) -> None:
        self.refresh(parameters)
    
    def refresh(self, parameters: proj_utils.Parameters) -> None:
        self.known_blocks = dict()
        self.pos = parameters.start
        self.path = [self.pos]
        self.hcells = []
        self.heuristic_i = 0
        self.heuristic = self.heuristics[self.heuristic_i]
        self.dir = self.DOWN
        self.xs, self.ys = parameters.xs, parameters.ys
        self.end = parameters.end
    def next_heuristic(self):
        self.heuristic_i += 1
        if self.heuristic_i >= len(self.heuristics):
            self.heuristic_i = 0
        self.heuristic = self.heuristics[self.heuristic_i]
    def triangle(self, screen: pygame.Surface, cell_size, failure=False):
        # (1,0) (0,1) (0,-1)
        tip = pygame.Vector2(cos(self.dir), sin(self.dir))
        left = pygame.Vector2(-sin(self.dir), cos(self.dir))
        right = pygame.Vector2(sin(self.dir), -cos(self.dir)) 
        points = [(self.pos+(i*0.5)+(0.5,0.5))*cell_size for i in [tip,left,right]]
        color = 'red' if failure else 'blue'
        pygame.draw.polygon(screen, color, points)

    def valid_step_cost(self, a:Vector2, b:Vector2, blocks:dict):
        step = b-a
        validate = lambda i: proj_utils.valid_cell(i, self.xs, self.ys, blocks)
        if abs(step.x) + abs(step.y) == 1:
            return 1 if validate(b) else None
        elif abs(step.x) + abs(step.y) == 2:
            return sqrt(2) if validate(b)and validate(Vector2(a.x, b.y)) and validate(Vector2(b.x, a.y)) else None
    def neighbors(self, cell: Vector2):
        return [cell + self.next_cell[dir] for dir in self.dirs]
        
    def huristic_path(self):
        heuristic = self.heuristic
        self.hcells = []
        hashify = lambda i: (i.x, i.y)
        vectify = lambda i: Vector2(i[0], i[1])
        q = [(0+heuristic(self.pos, self.end), 0, random.random(), hashify(self.pos), None)] # cost, cur, prev
        popped = dict()
        while q:
            _, cost, _, cur, prev = heapq.heappop(q)
            if cur in popped: continue
            prev = vectify(prev) if prev is not None else None
            popped[cur]=prev
            cur = vectify(cur)
            self.hcells.append(cur)
            if cur == self.end: break
            neighbors = self.neighbors(cur)
            for n in neighbors:
                c = self.valid_step_cost(cur, n, self.known_blocks)
                if not c: continue
                heapq.heappush(q, (cost+c+heuristic(n, self.end), cost+c, random.random(), hashify(n), hashify(cur)))

        if cur != self.end: return []
        path = [cur]
        popped.pop(hashify(self.pos), None)
        while hashify(path[-1]) in popped:
            path.append(popped[hashify(path[-1])])
        return [i for i in reversed(path)]
        # return [self.pos+[0.5,0.5], self.end+[0.5,0.5]]
    
    def stepable(self, a:Vector2, b:Vector2, actual_blocks):
        blocked = False
        if b.x in actual_blocks and b.y in actual_blocks[b.x]:
            self.known_blocks.setdefault(b.x, set()).add(b.y)
            blocked = True
        step = b - a
        diagonal = abs(step.x) + abs(step.y) == 2
        if not diagonal and not blocked:
            return True
        # (D,b) (d,B) (D,B)
        if not diagonal:
            return False
        # (D,b) (D,B)
        if a.x in actual_blocks and b.y in actual_blocks[a.x]:
            self.known_blocks.setdefault(a.x, set()).add(b.y)
            blocked = True
        if b.x in actual_blocks and a.y in actual_blocks[b.x]:
            self.known_blocks.setdefault(b.x, set()).add(a.y)
            blocked = True
        return not blocked

    def step(self, actual_blocks):
        path = self.huristic_path()
        if len(path) < 2: return
        next_cell = path[1]
        # turn to face the correct direction
        while self.pos + self.next_cell[self.dir] != next_cell:
            # print(f"turning {self.pos} -> {next_cell}")
            self.dir = self.next_dir[self.dir]
        # Check blocks
        if not self.stepable(self.pos, next_cell, actual_blocks):
            return
        self.pos = next_cell
        self.path.append(self.pos)

        pass

    def draw(self, screen: pygame.Surface):
        cell_size = proj_utils.calc_cell_size(self.xs, self.ys, screen)
        hpath = self.huristic_path()
        for hcell in self.hcells:
            surf = pygame.Surface((cell_size, cell_size))
            surf.fill('green')
            surf.set_alpha(50)
            screen.blit(surf, hcell*cell_size)
        failure = self.pos != self.end and len(hpath) < 2
        if len(hpath) > 1:
            pygame.draw.lines(screen, 'green4', False, [cell_size*(i+(0.5, 0.5)) for i in hpath])
        if len(self.path) > 1:
            pygame.draw.lines(screen, 'blue', False, [cell_size*(i+(0.5, 0.5)) for i in self.path])
        self.triangle(screen, cell_size, failure)
        proj_utils.draw_blocks(screen, self.known_blocks, cell_size, 'black')
