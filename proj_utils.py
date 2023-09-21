from typing import Any
import pygame
import random

class Parameters:
    def __init__(self, xs=50, ys=50, density=0.2) -> None:
        self.xs = xs
        self.ys = ys
        self.density = density
        self.refresh()

    def refresh(self, xs=None, ys=None, density=None) -> None:
        if xs is not None: self.xs = xs
        if ys is not None: self.ys = ys
        if density is not None: self.density = density
        self.blocks, _ = make_grid(self.xs, self.ys, self.density)
        self.start = random_loc(self.xs, self.ys, self.blocks)
        self.end = random_loc(self.xs, self.ys, self.blocks)

def draw_background(screen, parameters:Parameters, color_bg='white', color_bk='grey50'):

    xs, ys, blocks = parameters.xs, parameters.ys, parameters.blocks
    cell_size = calc_cell_size(xs, ys, screen)
    pygame.draw.rect(screen, color_bg, pygame.Rect((0, 0), (xs*cell_size, ys*cell_size)))
    draw_blocks(screen, blocks, cell_size, color_bk)
    # for x in blocks:
    #     for y in blocks[x]:
    #         _x, _y = cell_size*x, cell_size*y
    #         pygame.draw.rect(screen, color_bk, pygame.Rect((_x, _y), (cell_size, cell_size)))
    
    start, end = parameters.start, parameters.end
    pygame.draw.circle(screen, 'blue', (start+[0.5]*2)*cell_size, cell_size*0.3)
    pygame.draw.circle(screen, 'green', (end+[0.5]*2)*cell_size, cell_size*0.3)

def draw_blocks(screen, blocks, cell_size, color):
    for x in blocks:
        for y in blocks[x]:
            _x, _y = cell_size*x, cell_size*y
            pygame.draw.rect(screen, color, pygame.Rect((_x, _y), (cell_size, cell_size)))




def calc_cell_size(xs, ys, screen):
    return min(screen.get_width()/xs, screen.get_height()/ys)

def random_loc(xs, ys, blocked):
    _y = set()
    while not _y:
        x = random.randint(0, xs-1)
        _y = [y for y in range(ys) if x not in blocked or y not in blocked[x]]
    y = random.choice(list(_y))

    return pygame.Vector2(x, y)

    # return (random.randint(0, xs-1), random.randint(0, ys-1))

def valid_cell(cell, xs, ys, blocks):
    if cell.x < 0 or cell.y < 0: return False
    if cell.x >= xs: return False
    if cell.y >= ys: return False
    # blocked = self.grid[0]
    if cell.x in blocks and cell.y in blocks[cell.x]: return
    return True

# Lets make a grid of a given size
def make_grid(xs: int, ys: int, block_density: float=0.2):
    '''
    Function to make a grid in which the rover moves

    Parameters
    ---
        xs: number of cells on x axis
        ys: number of cells on y axis
        block_density: 0.0 to 1.0 density of blocked cells in grid
    
    Returns
    -------
        grid: (map of blocked cells, grid size)
    '''
    # Initially return empty grid of size xs*ys
    # Now randomly block some of the grids
    total = xs*ys
    blocked = random.sample([i for i in range(total)], int(total*block_density))
    blocked_cells = dict()
    for i in blocked:
        x = i%xs
        y = i//xs
        blocked_cells.setdefault(x, set()).add(y)
    return (blocked_cells, (xs, ys)) #(Blocks, size)

def make_square_grid(s: int, block_density: float = 0.2):
    return make_grid(s, s, block_density)

# Lets make a screen from a given grid
def draw_grid(screen:pygame.Surface, grid:tuple[dict, tuple[int, int]], known_blocks:dict):
    '''
    Function to make the screen for a given grid and cell size
    
    Parameters
    -----------
        grid: (Map of blocked cells, size of grid)
        cell_size: size of square cells of the grid
    '''
    grid_size = grid[1]
    grid_blocks = grid[0]
    # cell_size = min(screen.get_width()/grid_size[0], screen.get_height()/grid_size[1])
    cell_size = calc_cell_size(grid_size[0], grid_size[1], screen)
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            blocked = x in grid_blocks and y in grid_blocks[x]
            known_blocked = x in known_blocks and y in known_blocks[x]
            color = 'black' if known_blocked else 'grey50' if blocked else 'white'
            _x, _y = x*cell_size, y*cell_size
            pygame.draw.rect(screen, color, pygame.Rect((_x, _y), (cell_size, cell_size)))

    
class Keyed:
    def __init__(self) -> None:
        self.keys = set()
        self.pressed = dict() # key -> pressed
        self.action = dict() # key -> lambda
    def add_action(self, key: int, action):
        self.keys.add(key)
        self.pressed[key] = False
        self.action[key] = action
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pressed_key = pygame.key.get_pressed()
        for key in self.keys:
            if pressed_key[key] and not self.pressed[key]:
                self.action[key]()
                self.pressed[key] = True
            elif self.pressed[key] and not pressed_key[key]:
                self.pressed[key] = False

def cell_coord(pos:pygame.Vector2, screen, xs, ys):
    cell_size = calc_cell_size(xs, ys, screen)
    x = pos[0] // cell_size
    y = pos[1] // cell_size
    return pygame.Vector2(x,y)

def move_to_cell(cell: pygame.Vector2, screen, xs, ys):
    cell_size = calc_cell_size(xs, ys, screen)
    pygame.mouse.set_pos((cell+(0.5,0.5))*cell_size)
