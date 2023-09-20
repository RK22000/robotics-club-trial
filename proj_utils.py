import pygame
import random

def calc_cell_size(xs, ys, screen):
    return min(screen.get_width()/xs, screen.get_height()/ys)

def random_loc(xs, ys, blocked):
    _y = set()
    while not _y:
        x = random.randint(0, xs-1)
        _y = [y for y in range(ys) if y not in blocked[x]]
    y = random.choice(list(_y))

    return (x, y)

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

    

