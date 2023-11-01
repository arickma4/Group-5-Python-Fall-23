import pygame, sys
from pygame.locals import *
# set up pygame
pygame.init()
# set up the window
windowSurface = pygame.display.set_mode((0, 0))
pygame.display.set_caption('Jets! V0')
# run the game loop
Run = True
while Run:
    for event in pygame.event.get():
        if event.type == QUIT:
            Run = False
        if event.type == KEYDOWN and K_ESCAPE:
            Run = False
pygame.quit()
sys.exit()
