import pygame
import os


def kr(x, y): 
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 25, 5)


pygame.init()
width = 320
height = 920
screen = pygame.display.set_mode((width, height))
x, y = 240, 10
running = True
moving_left = False
moving_right = False
clock = pygame.time.Clock()
a = 0.01

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    if moving_left:
        x -= 0.1
    if moving_right:
        x += 0.1 

    a += 0.01
    y += (100 + a) * clock.tick() / 1000 
    screen.fill((0, 0, 0)) 
    if x > width - 25:
        x = width - 25
    if x < 25:
        x = 25
    kr(x, y)
    pygame.display.flip()
    if y >= height - 25:
        running = False
