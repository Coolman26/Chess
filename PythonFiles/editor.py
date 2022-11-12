import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame

def editor(vars):
    screen = vars["screen"]
    screen.fill((0, 0, 0))