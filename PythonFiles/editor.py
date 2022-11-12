import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame

def editor(vars):
    screen = vars["screen"]
    running = True
    while running:
        screen.fill((255, 0, 0))
        eventGet = pygame.event.get()
        for event in eventGet:
            if event.type == pygame.QUIT:
                running = False