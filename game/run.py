# code game loops and render stuff
from typing import Callable
import pygame

from body.gene import ENV_SEED, GEN_SEED
from algo.projection import CAMERA

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
                    CAMERA.rot.x += 20
                if event.key == pygame.K_DOWN:
                    CAMERA.rot.x -= 20
                if event.key == pygame.K_RIGHT:
                    CAMERA.rot.y += 20
                if event.key == pygame.K_LEFT:
                    CAMERA.rot.y -= 20

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
    n_grown = 0
    n_cap = 150
    i = 0

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            CAMERA.rot.y -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            CAMERA.rot.y += 5
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            CAMERA.rot.x -= 5
        if pygame.key.get_pressed()[pygame.K_UP]:
            CAMERA.rot.x += 5
        if pygame.key.get_pressed()[pygame.K_MINUS]:
            CAMERA.zoom *= 1.05
        if pygame.key.get_pressed()[pygame.K_EQUALS]:
            CAMERA.zoom /= 1.05

        reset = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    interval = 3
                if event.key == pygame.K_SPACE:
                    # Reset creature
                    print(f"That was {GEN_SEED=}, {ENV_SEED=}!")
                    reset = True
                    n_grown = 0
                if event.key == pygame.K_r:
                    # Reset camera angle
                    CAMERA.rot.scale_to_length(0)
                if event.key == pygame.K_p:
                    paused = not paused
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    interval = 30

        background(screen)

        grow = i % interval == 0 and not paused and n_grown < n_cap
        if grow:
            n_grown += 1

        render(screen, grow, reset)

        pygame.display.flip()
        clock.tick(FPS)

        i += 1

    pygame.quit()
