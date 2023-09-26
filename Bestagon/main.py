import pygame
import honeycomb
from bee0 import Bee


pygame.init()
size = (1280, 720)
size = (500, 500)
honeycomb.screen = pygame.display.set_mode(size, pygame.SRCALPHA|pygame.RESIZABLE)
honeycomb.newComb()
bee = Bee()


clock = pygame.time.Clock()
running = True
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
    bee.step()
    honeycomb.screen.fill('orange')
    honeycomb.draw()
    bee.draw()
    pygame.display.flip()
    clock.tick(8)