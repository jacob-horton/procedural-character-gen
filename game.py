# code game loops and render stuff
from typing import Callable
import pygame

FPS = 30

def background(screen: pygame.Surface):
    screen.fill("white")

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

        background(screen)
        render(space)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()