import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
pygame.font.init()
font = pygame.font.SysFont('Product Sans', 60)
 
# create a text surface object,
# on which text is drawn on it.
text = font.render('Chess Editor', True, (222,202,175)) 
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
 
# set the center of the rectangular object.


def editor(vars):
    screen = vars["screen"]
    screen.fill((169,126,92))
    width = screen.get_width()
    height = screen.get_height()
    textRect.center = (width // 2, 45)
    screen.blit(text, textRect)

    
    

    