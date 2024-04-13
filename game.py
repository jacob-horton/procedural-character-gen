# code game loops and render stuff
from typing import Callable
import pygame

FPS = 1

def background(screen: pygame.Surface):
    screen.fill("white")

def run(screen: pygame.Surface, clock: pygame.Clock, render: Callable[..., None]):
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        background(screen)
        render()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()