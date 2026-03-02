import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Cubes")

# Cube settings
cube_size = 30
num_cubes = 5
cubes = []
for _ in range(num_cubes):
    x = random.randint(0, WIDTH - cube_size)
    y = random.randint(0, HEIGHT - cube_size)
    dx = random.choice([-3, 3])
    dy = random.choice([-3, 3])
    cubes.append([x, y, dx, dy])

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Black background

    for cube in cubes:
        cube[0] += cube[2]
        cube[1] += cube[3]

        # Bounce off walls
        if cube[0] < 0 or cube[0] > WIDTH - cube_size:
            cube[2] *= -1
        if cube[1] < 0 or cube[1] > HEIGHT - cube_size:
            cube[3] *= -1

        pygame.draw.rect(screen, (255, 0, 0), (cube[0], cube[1], cube_size, cube_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()