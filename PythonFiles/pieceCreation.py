import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

class Piece():
    def __init__(self, color, type, position, name, vars) -> None:
        self.position = position
        self.color = color
        self.type = type
        print()
        self.png = loadpiece(color + type, vars)
        self.follow = False
        self.name = name
        vars["board"][position[0] + str(position[1])] = name
        if type == "pawn":
            self.movedTwo = False

    def moveTo(self, XY):
        self.position = [XY[0], int(XY[1])]

def imgload(img): 
    return pygame.image.load(img)

def startscolor(name):
    for color in ["black", "golden", "red", "white"]:
        if name.lower().startswith(color):
            return [True, color.capitalize()]

    return [False]

def endspiece(name, vars):
    for piece in vars["settings"]["pieces"]:
        if name.lower().endswith(piece):
            return [True, piece.capitalize()]
    return [False]

def loadpiece(name, vars):
    start = startscolor(name)
    end = endspiece(name, vars)
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