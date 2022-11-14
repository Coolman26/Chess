import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 45)
 
# create a text surface object,
# on which text is drawn on it.
text = font.render('Chess Editor', True, (28, 144, 147)) 
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
 
# set the center of the rectangular object.


def editor(vars):
    screen = vars["screen"]
    screen.fill((89, 22, 160))
    width = screen.get_width()
    height = screen.get_height()
    textRect.center = (width // 2, 60)
    screen.blit(text, textRect)

    
    

    