# code game loops and render stuff
from typing import Callable
import pygame
from pygame import Vector3

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


def run_presentation(
    screen: pygame.Surface, clock: pygame.time.Clock, render: Callable[..., None]
):
    running = True
    interval = 30
    paused = False
    i = 0

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        space = False
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            ROT.y -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            ROT.y += 5
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            ROT.x -= 5
        if pygame.key.get_pressed()[pygame.K_UP]:
            ROT.x += 5

        reset = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # TODO: reset
                    pass
                if event.key == pygame.K_RETURN:
                    interval = 3
                if event.key == pygame.K_SPACE:
                    # Reset creature
                    reset = True
                if event.key == pygame.K_r:
                    # Reset camera angle
                    ROT.scale_to_length(0)
                if event.key == pygame.K_p:
                    paused = not paused
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    interval = 30

        background(screen)
        render(screen, i % interval == 0 and not paused, reset)

        pygame.display.flip()
        clock.tick(FPS)

        i += 1

    pygame.quit()
