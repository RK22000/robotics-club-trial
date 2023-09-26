import pygame
from math import sin, pi, cos
import random

side = 50
buffer = 1.1
screen: pygame.Surface = None
maxX = lambda: (screen.get_width()-0.5*(side*buffer))//(1.5*side*buffer)
maxY = lambda: 2*(screen.get_height()//(sin(pi/3)*side*buffer*2))-1
def onTheChart(cell):
    return (
        cell[0] >= 0 and
        cell[1] >= 0 and
        cell[0] < maxX() and
        cell[1] < maxY()
    )

def draw_cell(cell: pygame.Vector2, color:pygame.Color):
    surf = pygame.Surface(pygame.Vector2(2.0, 2*sin(pi/3))*side, pygame.SRCALPHA)
    pygame.draw.polygon(surf, color, [ pygame.Vector2(*i)*side for i in [
        (0.5, 0),
        (1.5, 0),
        (2, sin(pi/3)),
        (1.5, 2*sin(pi/3)),
        (0.5, 2*sin(pi/3)),
        (0, sin(pi/3)),
    ]])
    color = pygame.Color(color)
    surf.set_alpha(color.a)
    cord = pygame.Vector2(cell)
    cord.x *= 1.5
    cord.y *= sin(pi/3)
    cord *= (side*buffer)
    screen.blit(surf, cord)



def neighbours(cell):
    return [j for j in [(cell[0]+i[0],cell[1]+i[1]) for i in [
        (1,1),
        (0,2),
        (-1,1),
        (-1,-1),
        (0,-2),
        (1,-1)
        ]] if onTheChart(j)]

block_density = 0.0
blocks = set()
def increase_density(): 
    global block_density
    block_density = min(block_density+0.1, 0.9)
    generate_blocks()
def decrease_density(): 
    global block_density
    block_density = max(block_density-0.1, 0.0)
    generate_blocks()
def generate_blocks():
    global blocks
    blocks = set(random.sample(list(all_cells()), int(block_density*len(all_cells()))))
    generate_start_and_goals()

start=(0,0)
goals=set([(1,1)])
ngoals = 2
def generate_start_and_goals():
    global start, goals
    start = random.choice(list(all_cells()-blocks))
    goals = random.sample(list(all_cells()-blocks-set([start])), ngoals)

def all_cells():
    if not hasattr(all_cells, 'state'): all_cells.state = None
    if all_cells.state == (screen.get_width(), screen.get_height(), side): 
        # print('Same cells')
        return all_cells.cells
    # else:
    #     print('Diff cells')
    cells = set()
    q = [(0,0)]
    while q:
        cell = q.pop()
        if cell in cells: continue
        cells.add(cell)
        neigh = neighbours(cell)
        q.extend(neigh)
    all_cells.cells = cells
    all_cells.state = (screen.get_width(), screen.get_height(), side)
    generate_blocks()
    generate_start_and_goals()
    return cells


def draw(known_block=set()):
    for cell in all_cells():
        color = 'orange' if cell in blocks else 'white'
        color = 'black' if cell in known_block else color
        color = 'blue' if cell == start else color
        color = 'green' if cell in goals else color
        draw_cell(cell, pygame.Color(color))

def rotate(cell: pygame.Vector2, dir: float) -> pygame.Vector2:
    cell = pygame.Vector2(cell)
    return pygame.Vector2(cell.x*cos(dir)-cell.y*sin(dir), cell.x*sin(dir)+cell.y*cos(dir))

def draw_path(path: list[pygame.Vector2], color: pygame.Color):
    color = pygame.Color(color)
    path = [(pygame.Vector2(1.5*x, y*sin(pi/3))*buffer+(1,sin(pi/3)))*side for x,y in path]
    pygame.draw.lines(screen, color, closed=False, points=path)

def draw_bee(cell: pygame.Vector2, dir: float, color):
    surf = pygame.Surface(pygame.Vector2(2.0, 2*sin(pi/3))*side, pygame.SRCALPHA)
    pygame.draw.polygon(surf, color, [ (rotate(i, dir)+(1,sin(pi/3)))*side for i in [
        (0, -sin(pi/3)),
        (-1, 0),
        (1, 0)
    ]])
    color = pygame.Color(color)
    surf.set_alpha(color.a)
    cord = pygame.Vector2(cell)
    cord.x *= 1.5
    cord.y *= sin(pi/3)
    cord *= (side*buffer)
    # cord.y -= side*(buffer-1)
    screen.blit(surf, cord)

def newComb():
    all_cells.state = None
    all_cells()

    


