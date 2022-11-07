import json
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from PythonFiles.pieceMovement import canCastle, canMove, castle
from PythonFiles.pieceCreation import imgload, loadpiece, numberOf
from PythonFiles.chessGameStates import inCheck, inTie




# initializing the constructor
pygame.init()


class Piece():
    def __init__(self, color, type, position, name, follow=False) -> None:
        self.position = position
        self.color = color
        self.type = type
        self.png = loadpiece(color + type, globalVariables())
        self.follow = follow
        self.name = name
        board[position[0] + str(position[1])] = name
        if type == "pawn":
            self.movedTwo = False

    def moveTo(self, XY):
        self.position = [XY[0], int(XY[1])]


def nextTurn():
    global turn, board, pieces
    turn += 1
    for x in range(boardSize):
        for y in range(boardSize):
            board[alphabet[x] + str(y+1)] = ""
    for piece in pieces:
        if pieces[piece] != "":
            pieces[piece].position = [
                alphabet[7 - alphabet.index(pieces[piece].position[0])], 9 - pieces[piece].position[1]]
            board[pieces[piece].position[0] +
                  str(int(pieces[piece].position[1]))] = piece

def globalVariables():
    return {
        "board":board,
        "topColor":topColor,
        "bottomColor":bottomColor,
        "pieces": pieces,
        "boardSize": boardSize,
        "overRideCanMove": overRideCanMove,
        "squareSize": squareSize,
        "screenDems": screenDems,
        "promotion": promotion,
        "screen": screen,
        "tileColor1": tileColor1,
        "tileColor2": tileColor2,
        "promotionPieces": promotionPieces
    }

def reset():
    global board, pieces, delete, check, tie, overRideCanMove, removePiece, overRideTurns, promotion, turn, winner
    board = {}
    delete = []
    check = None
    tie = False
    overRideCanMove = False
    removePiece = False
    overRideTurns = False
    promotion = ""
    turn = 1
    winner = ""
    for x in range(boardSize):
        for y in range(boardSize):
            board[alphabet[x] + str(y+1)] = ""

    pieces = {}
    for i in range(boardSize):
        for piece in range(len(settings["Row" + str(i+1)])):
            PieceName = settings["Row" + str(i+1)][::-1][piece]
            if PieceName != "":
                PieceType = PieceName[3:] if PieceName.startswith(
                    "top") else PieceName[6:]
                PieceColor = topColor if PieceName.startswith(
                    "top") else bottomColor
                PieceName = PieceColor + PieceType + \
                    numberOf(PieceColor + PieceType, pieces.keys())
                pieces[PieceName] = Piece(PieceColor, PieceType, [alphabet[piece], i+1], PieceName)

    


# Base Variables of Game
settings = json.load(open('profile.json'))
boardSize = settings["boardSize"]
screenDems = [800, 800]
developer = True 
topColor = settings["topColor"] 
bottomColor = settings["bottomColor"]
promotionPieceTypes = ["bishop", "rook", "knight", "queen"]
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
squareSize = screenDems[0]/boardSize 
tileColor1 = settings["tileColor1"]
tileColor2 = settings["tileColor2"]

# Setting the screen up
screen = pygame.display.set_mode(screenDems)
pygame.display.set_caption("Chess")  
icon = imgload("assets/icon.png")
pygame.display.set_icon(icon)

# Importing Promotion Pieces
promotionPieces = {}
for x in range(2):
    for y in range(len(promotionPieceTypes)):
        piece = imgload("assets/GamePieces/" + (topColor if x ==
                        1 else bottomColor).capitalize() + promotionPieceTypes[y].capitalize() + ".png")
        promotionPieces[(topColor if x == 1 else bottomColor) + str(y)] = pygame.transform.smoothscale(
            piece, [squareSize-10, screenDems[1]/boardSize-20])

# Importing logos
winnerLogo = imgload("assets/EndingPictures/Winner.jpg")  
winnerLogo = pygame.transform.smoothscale(
    winnerLogo, [screenDems[0], screenDems[1]//2])
loserLogo = imgload("assets/EndingPictures/Loser.jpg")  
loserLogo = pygame.transform.smoothscale(
    loserLogo, [screenDems[0], screenDems[1]//2])
tieLogo = imgload("assets/EndingPictures/Tie.jpg") 
tieLogo = pygame.transform.smoothscale(
    tieLogo, [screenDems[0], screenDems[1]])

reset()


running = True
while running:
    print(promotion)
    mouseXY = pygame.mouse.get_pos() 
    mousePressed = pygame.mouse.get_pressed()

    if delete:  # This deletes a piece in pieces if the delete list has something in it.
        # I did this because it activates inside of a for loop and I can't delete inside the for loop.
        del pieces[delete[0]]
        delete = []

    # This changes any pawn that has movedTwo equal to True(which means they have moved two spaces) to equal False if it has been more than one turn.
    for piece in pieces:
        if pieces[piece].type == "pawn":
            if pieces[piece].movedTwo != False:
                if turn - 1 == pieces[piece].movedTwo[1]:
                    pieces[piece].movedTwo = False

    # This checks if the game is inTie if it is then it checks if one side is in check.
    if not removePiece and promotion != "":
        # If they are in check then it is a checkmate and it ends.
        if inTie(globalVariables()):
            if check != None:
                winner = check
            else:
                tie = True

    # Loads the board tiles
    for y in range(boardSize):
        for x in range(boardSize):
            xEven = x % 2 == 0
            yEven = y % 2 == 0
            if (xEven and yEven) or (not xEven and not yEven):
                pygame.draw.rect(screen, tileColor2, [
                                 squareSize*(x), squareSize*(y), squareSize*(x+1), squareSize*(y+1)])
            else:
                pygame.draw.rect(screen, tileColor1, [
                                 squareSize*(x), squareSize*(y), squareSize*(x+1), squareSize*(y+1)])
                                 
    # Loads the pieces 
    for activePiece in pieces:
        if not pieces[activePiece].follow:
            x = boardSize - alphabet.index(pieces[activePiece].position[0])
            y = pieces[activePiece].position[1]
            screen.blit(pieces[activePiece].png, [
                        10+((x-1)*squareSize), (y-1)*(screenDems[1]/boardSize)+10])
        else:
            screen.blit(pieces[activePiece].png, [
                        mouseXY[0]-(squareSize/3), mouseXY[1]-(screenDems[1]/boardSize/3)])

    # Deals with promotion
    if promotion != "":
        promotionPiece = 0
        newX = boardSize - \
            alphabet.index(promotion[0]) - (3 if promotion[0] != "G" else 1)
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

    # Loads the winning and losing logo
    if winner != "":
        if winner == bottomColor:
            screen.blit(winnerLogo, [0, 0])
            screen.blit(loserLogo, [0, screenDems[1]//2])
        else:
            screen.blit(loserLogo, [0, 0])
            screen.blit(winnerLogo, [0, screenDems[1]//2])

    # Loads the tie logo
    if tie:
        screen.blit(tieLogo, [0, 0])

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if promotion == "":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not removePiece:
                    for piece in pieces:
                        if (turn % 2 == 0 if pieces[piece].color == topColor else turn % 2 == 1) or overRideTurns:
                            if mouseXY[0] // squareSize + 1 == (boardSize - alphabet.index(pieces[piece].position[0])) and mouseXY[1] // squareSize + 1 == pieces[piece].position[1]:
                                pieces[piece].follow = True
                else:
                    if not board[alphabet[int(boardSize - mouseXY[0] // squareSize - 1)] + str(int(mouseXY[1] // squareSize + 1))] == "":
                        del pieces[board[alphabet[int(
                            boardSize - mouseXY[0] // squareSize - 1)] + str(int(mouseXY[1] // squareSize + 1))]]
                        board[alphabet[int(boardSize - mouseXY[0] // squareSize - 1)] +
                              str(int(mouseXY[1] // squareSize + 1))] = ""
            elif event.type == pygame.MOUSEBUTTONUP:
                for piece in pieces:
                    moveTo = [alphabet[int(
                        boardSize - mouseXY[0] // squareSize - 1)], mouseXY[1] // squareSize + 1]
                    if pieces[piece].follow and not pieces[piece].position == moveTo and canMove(piece, moveTo, globalVariables()):
                        if check == None:
                            if turn % 2 == 1:
                                bottomColorCheckCounter = 0
                            else:
                                topColorCheckCounter = 0

                        firstLocation = pieces[piece].position
                        pieces[piece].follow = False

                        if canCastle(piece, moveTo, globalVariables()):
                            castle(piece, moveTo, globalVariables())

                        elif not board[moveTo[0] + str(int(moveTo[1]))] == "":
                            board[pieces[piece].position[0] +
                                  str(int(pieces[piece].position[1]))] = ""
                            delete = [board[moveTo[0] + str(int(moveTo[1]))]]
                            if pieces[board[moveTo[0] + str(int(moveTo[1]))]].type == "king":
                                winner = pieces[board[moveTo[0] +
                                                      str(int(moveTo[1]))]].color
                                break
                            pieces[board[moveTo[0] + str(int(moveTo[1]))]] = ""
                            pieces[piece].moveTo(moveTo)

                        else:
                            board[pieces[piece].position[0] +
                                  str(int(pieces[piece].position[1]))] = ""
                            pieces[piece].moveTo(moveTo) 
                            board[moveTo[0] +
                                  str(int(moveTo[1]))] = pieces[piece].name

                        checkState = inCheck(globalVariables())
                        if (checkState != None and check != None) or (checkState == pieces[piece].color):
                            pieces[piece].moveTo(firstLocation)
                            board[pieces[piece].position[0] +
                                  str(int(pieces[piece].position[1]))] = pieces[piece].name
                            board[moveTo[0] + str(int(moveTo[1]))] = ""
                            break
                        elif checkState != None:
                            check = checkState
                        elif checkState == None and check != None:
                            check = None
                            if turn % 2 == 1:
                                bottomColorCheckCounter += 1
                            else:
                                topColorCheckCounter += 1
                        
                        if pieces[piece].type == "pawn":
                            print(pieces[piece].position[1])
                            if pieces[piece].position[1] == 1:
                                promotion = pieces[piece].position + \
                                    [pieces[piece].color]
                            if abs(firstLocation[1] - int(moveTo[1])) == 2:
                                pieces[piece].movedTwo = [True, turn+1]
                            if abs(alphabet.index(firstLocation[0]) - alphabet.index(moveTo[0])) == 1 and board[moveTo[0] + str(int(moveTo[1]))] == "":
                                delete = [
                                    board[moveTo[0] + str(int(moveTo[1])+(1 if pieces[piece].color == bottomColor else -1))]]
                                board[moveTo[0] + str(int(moveTo[1])-1)] = ""
                        nextTurn()
                        
                        break
                    else:
                        pieces[piece].follow = False
            elif pygame.key.get_pressed()[pygame.K_LCTRL] and developer:
                developerControl = input("What would you like to do? ")
                if developerControl.lower() == "override canmove":
                    if not overRideCanMove:
                        overRideCanMove = True
                    else:
                        overRideCanMove = False
                elif developerControl.lower() == "remove piece":
                    if not removePiece:
                        removePiece = True
                    else:
                        removePiece = False
                elif developerControl.lower() == "override turns":
                    if not overRideTurns:
                        overRideTurns = True
                    else:
                        overRideTurns = False
                elif developerControl.lower() == "reset":
                    reset()
                elif developerControl.lower() == "print":
                    for piece in pieces:
                        print(pieces[piece].position)
        else:
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

    # updates the frames of the game
    pygame.display.update()

pygame.quit()
