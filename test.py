# Make a game using pygame
# By: Ben  
# Date: 1/1/2013

import pygame
from pygame.locals import *
import sys
import random

# Initialize pygame
pygame.init()

# Set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Game')

# Create game loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw the window onto the screen
    pygame.display.update()
