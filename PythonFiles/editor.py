import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
 
# create a text surface object,
# on which text is drawn on it.
text = font.render('GeeksForGeeks', True, "green", "blue")
 
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
 
# set the center of the rectangular object.


def editor(vars):
    screen = vars["screen"]
    screen.fill((255, 0, 0))
    width = screen.get_width()
    height = screen.get_height()
    textRect.center = (width // 2, height // 2)
    screen.blit(text, textRect)

    
    

    