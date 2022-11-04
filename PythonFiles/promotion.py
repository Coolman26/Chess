import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def promotionBoard(vars):
    boardSize = vars["boardSize"]
    promotion = vars["promotion"]
    screen = vars["screen"]
    tileColor1 = vars["tileColor1"]
    tileColor2 = vars["tileColor2"]
    squareSize = vars["squareSize"]
    screenDems = vars["screenDems"]
    promotionPieces = vars["promotionPieces"]
    promotionPiece = 0
    newX = boardSize - \
        alphabet.index(promotion[0]) - \
        (1 if alphabet.index(promotion[0]) != 0 else 3)
    for y in range(2):
        for x in range(2):
            xEven = x % 2 == 0
            yEven = y % 2 == 0
            if promotion[1] == 1:
                if (xEven and yEven) or (not xEven and not yEven):
                    pygame.draw.rect(screen, tileColor2, [
                                        squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, squareSize//2*(y+1) + squareSize//2*y, squareSize, squareSize])
                else:
                    pygame.draw.rect(screen, tileColor1, [
                                        squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, squareSize//2*(y+1) + squareSize//2*y, squareSize, squareSize])
                screen.blit(promotionPieces[promotion[2] + str(promotionPiece)], [squareSize//2*(
                    x+1) + squareSize//2*x + squareSize*newX + 10, squareSize//2*(y+1) + squareSize//2*y + 10])
            else:
                if (xEven and yEven) or (not xEven and not yEven):
                    pygame.draw.rect(screen, tileColor2, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, screenDems[1] - squareSize//2*(
                        y+1) + squareSize//2*y - (y+1) * squareSize, squareSize, squareSize])
                else:
                    pygame.draw.rect(screen, tileColor1, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, screenDems[1] - squareSize//2*(
                        y+1) + squareSize//2*y - (y+1)*squareSize, squareSize, squareSize])
                screen.blit(promotionPieces[promotion[2] + str(promotionPiece)], [squareSize//2*(x+1) + squareSize//2*x +
                            squareSize*newX + 10, screenDems[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)*squareSize + 10])
            promotionPiece += 1