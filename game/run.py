# code game loops and render stuff
from typing import Callable
import pygame

from algo.projection import ROT

FPS = 30


def background(screen: pygame.Surface):
    screen.fill(pygame.Color(220, 247, 255))


def run(screen: pygame.Surface, clock: pygame.time.Clock, render: Callable[..., None]):
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        space = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space = True
                if event.key == pygame.K_UP:
                    ROT.x += 20
                if event.key == pygame.K_DOWN:
                    ROT.x -= 20
                if event.key == pygame.K_RIGHT:
                    ROT.y += 20
                if event.key == pygame.K_LEFT:
                    ROT.y -= 20

        background(screen)
        render(screen, space)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
