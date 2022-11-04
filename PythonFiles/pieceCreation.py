import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame


def imgload(img): 
    return pygame.image.load(img)

def startscolor(name):
    for color in ["black", "golden", "red", "white"]:
        if name.lower().startswith(color):
            return [True, color.capitalize()]

    return [False]

def endspiece(name):
    for piece in ["bishop", "king", "knight", "pawn", "queen", "rook"]:
        if name.lower().endswith(piece):
            return [True, piece.capitalize()]
    return [False]

def loadpiece(name, vars):
    start = startscolor(name)
    end = endspiece(name)
    if start[0] and end[0]:
        piece = imgload("assets/GamePieces/" + start[1] + end[1] + ".png")
        piece = pygame.transform.smoothscale(piece, [vars["squareSize"]-10, vars["screenDems"][1]/vars["boardSize"]-20])
        return piece

def numberOf(key, list):
    x = 0
    for thing in list:
        if thing.startswith(key):
            x += 1
    return str(x)