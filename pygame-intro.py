import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0.001
res = 0.1

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
acc = pygame.Vector2(0, 0)
vel = pygame.Vector2(0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill('purple')
    player_pos += vel
    vel *= res
    vel += acc

    pygame.draw.circle(screen, 'red', player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        acc.y -= 300 * dt
    if keys[pygame.K_s]:
        acc.y += 300 * dt
    if keys[pygame.K_a]:
        acc.x -= 300 * dt
    if keys[pygame.K_d]:
        acc.x += 300 * dt

    pygame.display.flip()
    clock.tick(60)

pygame.quit()