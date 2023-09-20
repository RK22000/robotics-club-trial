from typing import Any
import proj_utils
import pygame
import rover1

def main():
    parameters = proj_utils.Parameters()
    rover = rover1.Rover(parameters)
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    # FPS = [4, 8, 15, 30, 60, 120]
    # fps = 0
    class FPS:
        def __init__(self) -> None:
            self.arr = [4, 8, 15, 30, 60, 120]
            self.i = 0
        def faster(self):
            self.i = min(len(self.arr)-1, self.i+1)
        def slower(self):
            self.i = max(0, self.i-1)
        def __call__(self, *args: Any, **kwds: Any) -> Any:
            return self.arr[self.i]
    fps = FPS()
    keyed = proj_utils.Keyed()
    keyed.add_action(
        pygame.K_RETURN,
        lambda: (parameters.refresh(), rover.refresh(parameters))
    )
    keyed.add_action(
        pygame.K_UP,
        lambda: (
            parameters.refresh(density=min(parameters.density+0.1, 0.9)), 
            rover.refresh(parameters)
            )
    )
    keyed.add_action(
        pygame.K_DOWN,
        lambda: (
            parameters.refresh(density=max(parameters.density-0.1, 0)),
            rover.refresh(parameters)
        )
    )
    keyed.add_action(
        pygame.K_RIGHT,
        fps.faster
    )
    keyed.add_action(
        pygame.K_LEFT,
        fps.slower
    )
    while running:
        keys = pygame.key.get_pressed()
        if pygame.QUIT in (e.type for e in pygame.event.get()) or keys[pygame.K_q]:
            running = False
        mb = pygame.mouse.get_pressed()
        if mb[0]:
            mpos = proj_utils.cell_coord(pygame.mouse.get_pos(), screen, parameters.xs, parameters.ys)
            if mpos != parameters.start:
                proj_utils.move_to_cell(mpos, screen, parameters.xs, parameters.ys)
                parameters.start = mpos
                rover.refresh(parameters)
        if mb[2]:
            mpos = proj_utils.cell_coord(pygame.mouse.get_pos(), screen, parameters.xs, parameters.ys)
            if mpos != parameters.end:
                proj_utils.move_to_cell(mpos, screen, parameters.xs, parameters.ys)
                parameters.end = mpos
                rover.refresh(parameters)
        keyed()

        screen.fill('purple')
        proj_utils.draw_background(screen=screen, parameters=parameters)
        rover.draw(screen)
        rover.step(parameters.blocks)

        pygame.display.flip()
        clock.tick(fps())
    
    

if __name__=='__main__':
    main()