import math
import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption('Pong')
pygame.mouse.set_visible(1)
font = pygame.font.Font(None, 36)
background = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()
done = False
exit_program = False

while not exit_program:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
