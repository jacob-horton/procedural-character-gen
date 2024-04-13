'''
the main script
'''
import pygame
import game

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

game.run(screen, clock)