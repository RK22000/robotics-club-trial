import pygame
import honeycomb
from bee1 import Bee
from memo import memo_bee


pygame.init()
size = (1280, 720)
size = (500, 500)
honeycomb.screen = pygame.display.set_mode(size, pygame.SRCALPHA|pygame.RESIZABLE)
honeycomb.newComb()
bees = [
    Bee(),
    Bee(name='A*', heuristic=lambda a,b: honeycomb.cell_dist(a,b))
]
beei = 0
bee = bees[beei]


clock = pygame.time.Clock()
tick = 8
running = True
count = 0
while running:
    keys = pygame.key.get_pressed()
    if pygame.QUIT in (e.type for e in pygame.event.get()) or keys[pygame.K_q]:
        running = False
    if keys[pygame.K_RETURN]:
        honeycomb.newComb()
        bee.refresh()
    if keys[pygame.K_EQUALS]:
        honeycomb.side = honeycomb.side*1.2
        honeycomb.newComb()
        bee.refresh()
    elif keys[pygame.K_MINUS]:
        honeycomb.side = honeycomb.side/1.2
        honeycomb.newComb()
        bee.refresh()
    if keys[pygame.K_UP]:
        honeycomb.increase_density()
        bee.refresh()
    elif keys[pygame.K_DOWN]:
        honeycomb.decrease_density()
        bee.refresh()
    if keys[pygame.K_RIGHT]:
        tick*=2
    elif keys[pygame.K_LEFT]:
        tick/=2
        if tick < 8: tick=8
    if keys[pygame.K_i]:
        bee.refresh()
        bee.blocks = honeycomb.blocks
    if keys[pygame.K_b]:
        beei+=1
        if beei >= len(bees): beei=0
        bee = bees[beei]
        bee.refresh()
    mb = pygame.mouse.get_pressed()
    mcell = honeycomb.coord_to_cell(pygame.mouse.get_pos())
    if mb[0]:
        honeycomb.start = mcell
    elif mb[2]:
        if mcell in honeycomb.goals:
            honeycomb.goals.remove(mcell)
            honeycomb.ngoals -= 1
        else:
            honeycomb.goals.add(mcell)
            honeycomb.ngoals += 1
    if mb[0] or mb[2]: bee.refresh()

    bee.step()
    count+=1
    honeycomb.screen.fill('orange')
    honeycomb.draw(bee.blocks)
    bee.draw()
    if keys[pygame.K_m]:
        memo_bee(bee)
    pygame.display.flip()
    clock.tick(tick)