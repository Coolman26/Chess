import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from PythonFiles.pieceMovement import nextTurn
from PythonFiles.pieceCreation import numberOf, Piece
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def promotionBoard(vars, eventGet, mouseXY):
    print(eventGet)
    boardSize = vars["boardSize"]
    promotion = vars["promotion"]
    screen = vars["screen"]
    tileColor1 = vars["tileColor1"]
    tileColor2 = vars["tileColor2"]
    squareSize = vars["squareSize"]
    promotionPieces = vars["promotionPieces"]
    pieces = vars["pieces"]
    promotionPieceTypes = vars["promotionPieceTypes"]
    promotionPiece = 0
    newX = boardSize - alphabet.index(promotion[0]) - (3 if promotion[0] != "G" else 1)
    for y in range(2):
        for x in range(2):
            tileX = squareSize//2*(x+1) + squareSize//2*x + squareSize*newX
            tileY =  squareSize//2*(y+1) + squareSize//2*y
            xEven = x % 2 == 0
            yEven = y % 2 == 0
            if (xEven and yEven) or (not xEven and not yEven):
                pygame.draw.rect(screen, tileColor2, [tileX, tileY, squareSize, squareSize])
            else:
                pygame.draw.rect(screen, tileColor1, [tileX, tileY, squareSize, squareSize])
            screen.blit(promotionPieces[promotion[2] + str(promotionPiece)], [tileX + 10, tileY + 10])
            promotionPiece += 1
    for event in eventGet:
        if event.type == pygame.MOUSEBUTTONUP:
            promotionPiece = 0
            for y in range(2):
                for x in range(2):
                    xEven = x % 2 == 0
                    yEven = y % 2 == 0
                    topLeftX = squareSize//2*(x+1) + squareSize//2*x + squareSize*newX
                    topLeftY = squareSize//2*(y+1) + squareSize//2*y
                    pieceName = promotion[2] + promotionPieceTypes[promotionPiece] + numberOf(promotion[2] + promotionPieceTypes[promotionPiece], pieces.keys())
                    if topLeftX <= mouseXY[0] <= topLeftX + squareSize and topLeftY <= mouseXY[1] <= topLeftY + squareSize:
                        pieces[pieceName] = Piece(promotion[2], promotionPieceTypes[promotionPiece], [
                                                    promotion[0], promotion[1]], pieceName, vars)
                        promotion = ""
                        vars["promotion"] = ""
                        break
                    promotionPiece += 1
                break
    if promotion == "":
        nextTurn(vars)
    