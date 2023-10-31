import pygame, sys
from pygame.locals import *
# set up pygame
pygame.init()
# set up the window
windowSurface = pygame.display.set_mode((0, 0))
pygame.display.set_caption('Jets! V0')
# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and K_ESCAPE:
            pygame.quit()
            sys.exit()
