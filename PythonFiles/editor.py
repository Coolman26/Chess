import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
pygame.font.init()
font = pygame.font.SysFont('Product Sans', 60)
 
text = font.render('Chess Editor', True, (222,202,175)) 
textRect = text.get_rect()
boardEditingIcon = pygame.image.load("assets\EditingIcons\BoardEditIcon.png")
boardEditingIcon = pygame.transform.smoothscale(boardEditingIcon, )

def editor(vars):
    screen = vars["screen"]
    screen.fill((169,126,92))
    width = screen.get_width()
    height = screen.get_height()
    textRect.center = (width // 2, 45)
    screen.blit(text, textRect)
    screen.blit(boardEditingIcon, (width//2-width//4, height//2-height//4))

    
    

    