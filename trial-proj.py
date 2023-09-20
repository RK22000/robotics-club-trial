import proj_utils
import pygame
import rover1

def main():
    new_parameters = lambda: proj_utils.Parameters()
    parameters = new_parameters()
    new_rover = lambda: rover1.Rover(parameters)
    rover = new_rover()
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    class Keyed:
        def __init__(self) -> None:
            self.entered, self.up, self.down = False, False, False
    keyed = Keyed()
    while running:
        keys = pygame.key.get_pressed()
        if pygame.QUIT in (e.type for e in pygame.event.get()) or keys[pygame.K_q]:
            running = False
        if keys[pygame.K_RETURN] and not keyed.entered:
            parameters = new_parameters()
            rover = new_rover()
            keyed.entered = True
        if keyed.entered and not keys[pygame.K_RETURN]:
            keyed.entered = False
        if keys[pygame.K_UP] and not keyed.up:
            parameters = proj_utils.Parameters(density=parameters.density+0.1)
            rover = new_rover()
            keyed.up = True
        if keyed.up and not keys[pygame.K_UP]:
            keyed.up = False
        if keys[pygame.K_DOWN] and not keyed.down:
            parameters = proj_utils.Parameters(density=parameters.density-0.1)
            rover = new_rover()
            keyed.down = True
        if keyed.down and not keys[pygame.K_DOWN]:
            keyed.down = False


        screen.fill('purple')
        proj_utils.draw_background(screen=screen, parameters=parameters)
        rover.draw(screen)
        rover.step(parameters.blocks)

        pygame.display.flip()
        clock.tick(4)
    
    
    # density = 0.2
    # make_grid = lambda den: proj_utils.make_square_grid(48, den)
    # grid = make_grid(density)
    # pygame.init()
    # screen = pygame.display.set_mode((1280, 720))
    # make_rover = lambda: rover0.Rover(
    #     grid=grid, 
    #     cell_size=proj_utils.calc_cell_size(*grid[1], screen),
    #     start=proj_utils.random_loc(*grid[1], grid[0]),
    #     end=proj_utils.random_loc(*grid[1], grid[0])
    #     # start=(0, 0),
    #     # end=(grid[1][0]-1, grid[1][1]-1)
    # )
    # rover = make_rover()
    # clock = pygame.time.Clock()
    # running = True
    # entered = False

    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #     screen.fill('purple')
    #     proj_utils.draw_grid(screen, grid, rover.known_blocks)
    #     rover.draw(screen)
    #     rover()
        
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_SPACE]:
    #         grid = make_grid(density)
    #         rover = make_rover()
    #     if keys[pygame.K_UP]:
    #         density = min(1.0, density+0.1)
    #         grid = make_grid(density)
    #         rover = make_rover()
    #     if keys[pygame.K_DOWN]:
    #         density = max(0.0, density-0.1)
    #         grid = make_grid(density)
    #         rover = make_rover()

        

    #     pygame.display.flip()
    #     clock.tick(30) # FPS

if __name__=='__main__':
    main()