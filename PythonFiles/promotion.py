import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from PythonFiles.pieceMovement import nextTurn
from PythonFiles.pieceCreation import numberOf
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def promotionBoard(vars, event, mouseXY):
    boardSize = vars["boardSize"]
    promotion = vars["promotion"]
    screen = vars["screen"]
    tileColor1 = vars["tileColor1"]
    tileColor2 = vars["tileColor2"]
    squareSize = vars["squareSize"]
    screenDems = vars["screenDems"]
    promotionPieces = vars["promotionPieces"]
    pieces = vars["pieces"]

    promotionPiece = 0
    newX = boardSize - alphabet.index(promotion[0]) - (3 if promotion[0] != "G" else 1)
    for y in range(2):
        for x in range(2):
            xEven = x % 2 == 0
            yEven = y % 2 == 0
            if (xEven and yEven) or (not xEven and not yEven):
                    pygame.draw.rect(screen, tileColor2, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, screenDems[1] - squareSize//2*(
                        y+1) + squareSize//2*y - (y+1) * squareSize, squareSize, squareSize])
            else:
                    pygame.draw.rect(screen, tileColor1, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, screenDems[1] - squareSize//2*(
                        y+1) + squareSize//2*y - (y+1)*squareSize, squareSize, squareSize])
            screen.blit(promotionPieces[promotion[2] + str(promotionPiece)], [squareSize//2*(x+1) + squareSize//2*x +
                            squareSize*newX + 10, screenDems[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)*squareSize + 10])
            promotionPiece += 1
    if event.type == pygame.MOUSEBUTTONUP:
                promotionPiece = 0
                for y in range(2):
                    for x in range(2):
                        xEven = x % 2 == 0
                        yEven = y % 2 == 0
                        pieceName = promotion[2] + promotionPieceTypes[promotionPiece] + numberOf(
                            promotion[2] + promotionPieceTypes[promotionPiece], pieces.keys())
                        if promotion[1] == 1:
                            if squareSize//2*(x+1) + squareSize//2*x + squareSize*newX <= mouseXY[0] <= squareSize//2*(x+1) + squareSize//2*x + squareSize*newX + squareSize and squareSize//2*(y+1) + squareSize//2*y <= mouseXY[1] <= squareSize//2*(y+1) + squareSize//2*y + squareSize:
                                pieces[pieceName] = Piece(promotion[2], promotionPieceTypes[promotionPiece], [
                                                          promotion[0], promotion[1]], pieceName)
                                promotion = ""
                                break
                        else:
                            if squareSize//2*(x+1) + squareSize//2*x + squareSize*newX <= mouseXY[0] <= squareSize//2*(x+1) + squareSize//2*x + squareSize*newX and screenDems[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1) * squareSize <= mouseXY[1] <= screenDems[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1) * squareSize + squareSize:
                                pieces[pieceName] = Piece(promotion[2], promotionPieceTypes[promotionPiece], [
                                                          promotion[0], promotion[1]], pieceName)
                                promotion = ""
                                break
                        promotionPiece += 1
                    break
    