import proj_utils
import pygame
import rover0

def main():
    density = 0.2
    make_grid = lambda den: proj_utils.make_square_grid(48, den)
    grid = make_grid(density)
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    make_rover = lambda: rover0.Rover(
        grid=grid, 
        cell_size=proj_utils.calc_cell_size(*grid[1], screen),
        start=proj_utils.random_loc(*grid[1], grid[0]),
        end=proj_utils.random_loc(*grid[1], grid[0])
        # start=(0, 0),
        # end=(grid[1][0]-1, grid[1][1]-1)
    )
    rover = make_rover()
    clock = pygame.time.Clock()
    running = True
    entered = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('purple')
        proj_utils.draw_grid(screen, grid, rover.known_blocks)
        rover.draw(screen)
        rover()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            grid = make_grid(density)
            rover = make_rover()
        if keys[pygame.K_UP]:
            density = min(1.0, density+0.1)
            grid = make_grid(density)
            rover = make_rover()
        if keys[pygame.K_DOWN]:
            density = max(0.0, density-0.1)
            grid = make_grid(density)
            rover = make_rover()

        

        pygame.display.flip()
        clock.tick(30) # FPS

if __name__=='__main__':
    main()