import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
from PythonFiles.pieceCreation import numberOf, imgload, loadpiece
from PythonFiles.pieceMovement import canMove, canCastle
from PythonFiles.chessGameStates import inCheck, inTie

# initializing the constructor
pygame.init()

class piece():
    def __init__(self, color, type, position, name, follow=False) -> None:
        self.position = position
        self.color = color
        self.type = type
        self.png = loadpiece(color + type, squareSize, SCREEN_DIMENSIONS, boardSize)
        self.follow = follow
        self.name = name
        board[position[0] + str(position[1])] = name
        if type == "pawn":
            self.movedTwo = False

## Base Variables of Game
SCREEN_DIMENSIONS = [800, 800] #How wide the screen is by how tall the screen is in pixels
developer = True #Whether or not you can hit left control to access developer commands
boardSize = 8 #How many squares for the length and width
topColor = "black" #Which color starts on the top of the board
bottomColor = "white" #Which color starts at the bottom of the board and goes first
promotionPieceTypes = ["bishop", "rook", "knight", "queen"] #Which pieces are available when a pawn is being promoted(must have a png to back it up)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" #The alphabet which the game uses
squareSize = SCREEN_DIMENSIONS[0]/boardSize #How large each square is

## Setting the game up
screen = pygame.display.set_mode(SCREEN_DIMENSIONS) #P
height, width = screen.get_height(), screen.get_width()
pygame.display.set_caption("Chess")
icon = imgload("assets/icon.png")
pygame.display.set_icon(icon)

winnerLogo = imgload("assets/EndingPictures/Winner.jpg")
winnerLogo = pygame.transform.smoothscale(winnerLogo, [SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]//2])
loserLogo = imgload("assets/EndingPictures/Loser.jpg")
loserLogo = pygame.transform.smoothscale(loserLogo, [SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]//2])
tieLogo = imgload("assets/EndingPictures/Tie.jpg")
tieLogo = pygame.transform.smoothscale(tieLogo, [SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]])

promotionPieces = {}


for x in range(2):
    for y in range(len(promotionPieceTypes)):
        Piece = imgload("assets/GamePieces/" + (topColor if x == 1 else bottomColor).capitalize() + promotionPieceTypes[y].capitalize() + ".png")
        promotionPieces[(topColor if x == 1 else bottomColor) + str(y)] = pygame.transform.smoothscale(Piece, [squareSize-10, SCREEN_DIMENSIONS[1]/boardSize-20])

# colors
SKY_BLUE = (125, 175, 255)
WHITE = (255, 255, 255)
LIGHT_GREY = (175, 175, 175)
DARK_GREY = (100, 100, 100)
LIGHT_GREEN = (63, 196, 47)
LIGHT_RED = (240, 36, 22)
DARK_GREEN = (49, 158, 36)
DARK_RED = (199, 30, 18)
DARK_BLUE = (21, 42, 176)
LIGHT_BLUE = (44, 71, 242)
DARK_ORANGE = (186, 172, 20)
LIGHT_ORANGE = (230, 212, 25)
BROWN = (169,126,92)
LIGHT_BROWN = (222,202,175)

def reset():
    global board, pieces, delete, check, tie, overRideCanMove, removePiece, overRideTurns, promotion, turn, winner
    board = {}
    for x in range(boardSize):
        for y in range(boardSize):
            board[alphabet[x] + str(y+1)] = ""

    pieces = {}
    topPieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
    for i in range(len(topPieces)):
        pieces[topColor + topPieces[i] + numberOf(topColor + topPieces[i], pieces.keys())] = piece(topColor, topPieces[i], [alphabet[boardSize-i - 1],1], topColor + topPieces[i] + numberOf(topColor + topPieces[i], pieces.keys()))
    for i in range(boardSize):
        pieces[topColor + "pawn" + str(i)] = piece(topColor, "pawn", [alphabet[boardSize-i - 1],2], topColor + "pawn" + str(i))
    bottomPieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
    for i in range(boardSize):
        pieces[bottomColor + "pawn" + str(i)] = piece(bottomColor, "pawn", [alphabet[boardSize-i - 1],7], bottomColor + "pawn" + str(i))
    for i in range(len(bottomPieces)):
        pieces[bottomColor + bottomPieces[i] + numberOf(bottomColor + bottomPieces[i], pieces.keys())] = piece(bottomColor, bottomPieces[i], [alphabet[boardSize-i - 1],8], bottomColor + bottomPieces[i] + numberOf(bottomColor + bottomPieces[i], pieces.keys()))
    delete = []
    check = None
    tie = False
    overRideCanMove = False
    removePiece = False
    overRideTurns = False
    promotion = ""
    turn = 1
    winner = ""
reset()

running = True
while running:
    if delete:
        del pieces[delete[0]]
        delete = []
    
    for Piece in pieces:
        if pieces[Piece].type == "pawn":
            if pieces[Piece].movedTwo != False:
                if turn - 1 == pieces[Piece].movedTwo[1]:
                    pieces[Piece].movedTwo = False
    if not removePiece:
        if inTie():
            if check != None:
                winner = check
            else:
                tie = True
    
    mouseXY = pygame.mouse.get_pos()
    for y in range(boardSize):
        for x in range(boardSize):
            xEven = x % 2 == 0
            yEven = y % 2 == 0
            if (xEven and yEven) or (not xEven and not yEven): 
                pygame.draw.rect(screen, LIGHT_BROWN, [squareSize*(x), squareSize*(y), squareSize*(x+1), squareSize*(y+1)])
            else: 
                pygame.draw.rect(screen, BROWN, [squareSize*(x), squareSize*(y), squareSize*(x+1), squareSize*(y+1)])
    for activePiece in pieces:
        if not pieces[activePiece].follow:
            x = boardSize - alphabet.index(pieces[activePiece].position[0])
            y = pieces[activePiece].position[1]
            screen.blit(pieces[activePiece].png, [10+((x-1)*squareSize), (y-1)*(SCREEN_DIMENSIONS[1]/boardSize)+10])
        else:
            screen.blit(pieces[activePiece].png, [mouseXY[0]-(squareSize/3), mouseXY[1]-(SCREEN_DIMENSIONS[1]/boardSize/3) ])
    if promotion != "":
        promotionPiece = 0
        if alphabet.index(promotion[0]) != 0:
            newX = boardSize - alphabet.index(promotion[0]) - 1
        else:
            newX = boardSize - alphabet.index(promotion[0]) - 3
        for y in range(2):
            for x in range(2):
                xEven = x % 2 == 0
                yEven = y % 2 == 0
                if promotion[1] == 1:
                    if (xEven and yEven) or (not xEven and not yEven): 
                        pygame.draw.rect(screen, LIGHT_BROWN, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, squareSize//2*(y+1) + squareSize//2*y, squareSize, squareSize])
                    else: 
                        pygame.draw.rect(screen, BROWN, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, squareSize//2*(y+1) + squareSize//2*y, squareSize, squareSize])
                    screen.blit(promotionPieces[promotion[2] + str(promotionPiece)], [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX + 10, squareSize//2*(y+1) + squareSize//2*y + 10])
                else:
                    if (xEven and yEven) or (not xEven and not yEven): 
                        pygame.draw.rect(screen, LIGHT_BROWN, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)* squareSize, squareSize, squareSize])
                    else: 
                        pygame.draw.rect(screen, BROWN, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)*squareSize, squareSize, squareSize])
                    screen.blit(promotionPieces[promotion[2] + str(promotionPiece)], [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX + 10, SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)*squareSize + 10])
                promotionPiece += 1
    mouse = pygame.mouse.get_pressed()
    if winner != "":
        if winner == bottomColor:
            screen.blit(winnerLogo, [0, 0])
            screen.blit(loserLogo, [0, SCREEN_DIMENSIONS[1]//2])
        else:
            screen.blit(loserLogo, [0, 0])
            screen.blit(winnerLogo, [0, SCREEN_DIMENSIONS[1]//2])
    if tie:
        screen.blit(tieLogo, [0, 0])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        if promotion == "":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not removePiece:
                    for piecessss in pieces:
                        if (turn % 2 == 0 if pieces[piecessss].color == topColor else turn % 2 == 1) or overRideTurns:
                            if mouseXY[0] // squareSize + 1 == (boardSize - alphabet.index(pieces[piecessss].position[0])) and mouseXY[1] // squareSize + 1 == pieces[piecessss].position[1]:
                                pieces[piecessss].follow = True
                else:
                    if not board[alphabet[int(boardSize - mouseXY[0] // squareSize - 1)] + str(int(mouseXY[1] // squareSize + 1))] == "":
                        del pieces[board[alphabet[int(boardSize - mouseXY[0] // squareSize - 1)] + str(int(mouseXY[1] // squareSize + 1))]] 
                        board[alphabet[int(boardSize - mouseXY[0] // squareSize - 1)] + str(int(mouseXY[1] // squareSize + 1))] = ""
            elif event.type == pygame.MOUSEBUTTONUP:
                if not removePiece:
                    for piecessss in pieces:
                        moveTo = [alphabet[int(boardSize - mouseXY[0] // squareSize - 1)], mouseXY[1] // squareSize + 1]
                        if pieces[piecessss].follow and not pieces[piecessss].position == moveTo and canMove(piecessss, moveTo, board, pieces, boardSize, bottomColor, overRideCanMove):
                            if board[moveTo[0] + str(int(moveTo[1]))] == "":
                                if check == None:
                                    if turn % 2 == 1:
                                        bottomColorCheckCounter = 0
                                    else:
                                        topColorCheckCounter = 0
                                firstLocation = pieces[piecessss].position
                                pieces[piecessss].follow = False
                                board[pieces[piecessss].position[0] + str(int(pieces[piecessss].position[1]))] = ""
                                pieces[piecessss].position = moveTo
                                board[moveTo[0] + str(int(moveTo[1]))] = pieces[piecessss].name
                                checkState = inCheck(pieces, board, overRideCanMove, bottomColor, topColor, boardSize)
                                if pieces[piecessss].type == "pawn" and pieces[piecessss].position[1] == (8 if pieces[piecessss].color == topColor else 1):
                                    promotion = pieces[piecessss].position + [pieces[piecessss].color]
                                if pieces[piecessss].type == "pawn" and abs(firstLocation[1] - int(moveTo[1])) == 2:
                                    pieces[piecessss].movedTwo = [True, turn+1]
                                if pieces[piecessss].type == "pawn" and abs(alphabet.index(firstLocation[0]) - alphabet.index(moveTo[0])) == 1:
                                    delete = [board[moveTo[0] + str(int(moveTo[1])+(1 if pieces[piecessss].color == bottomColor else -1))]]
                                    board[moveTo[0] + str(int(moveTo[1])+(-1 if pieces[piecessss].color == bottomColor else 1))] = ""
                                if (checkState != None and check != None) or (checkState == pieces[piecessss].color):
                                    pieces[piecessss].position = firstLocation
                                    board[pieces[piecessss].position[0] + str(int(pieces[piecessss].position[1]))] = pieces[piecessss].name
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
                                turn += 1
                                if inTie():
                                    tie = True
                                break
                            elif pieces[board[moveTo[0] + str(int(moveTo[1]))]].color != pieces[piecessss].color:
                                if check == None:
                                    if turn % 2 == 1:
                                        bottomColorCheckCounter = 0
                                    else:
                                        topColorCheckCounter = 0
                                pieces[piecessss].follow = False
                                board[pieces[piecessss].position[0] + str(int(pieces[piecessss].position[1]))] = ""
                                delete = [board[moveTo[0] + str(int(moveTo[1]))]]
                                if pieces[board[moveTo[0] + str(int(moveTo[1]))]].type == "king":
                                    winner = pieces[board[moveTo[0] + str(int(moveTo[1]))]].color
                                    break
                                pieces[board[moveTo[0] + str(int(moveTo[1]))]] = ""
                                pieces[piecessss].position = moveTo
                                board[moveTo[0] + str(int(moveTo[1]))] = pieces[piecessss].name
                                checkState = inCheck(pieces, board, overRideCanMove, bottomColor, topColor, boardSize)
                                if pieces[piecessss].type == "pawn" and pieces[piecessss].position[1] == (8 if pieces[piecessss].color == topColor else 1):
                                    promotion = pieces[piecessss].position + [pieces[piecessss].color]
                                if (checkState != None and check != None) or (checkState == pieces[piecessss].color):
                                    pieces[piecessss].position = firstLocation
                                    board[pieces[piecessss].position[0] + str(int(pieces[piecessss].position[1]))] = pieces[piecessss].name
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
                                turn += 1
                                if inTie():
                                    tie = True
                                break 
                            else:
                                pieces[piecessss].follow = False
                        elif board[moveTo[0] + str(int(moveTo[1]))] != "":
                            if canCastle(piecessss, moveTo, board, topColor, pieces, boardSize):
                                pieces[piecessss].follow = False
                                board[pieces[piecessss].position[0] + str(int(pieces[piecessss].position[1]))] = ""
                                if moveTo[0] == "A":
                                    pieces[piecessss].position = ["B" , pieces[piecessss].position[1]]
                                    board["B" + str(int(pieces[piecessss].position[1]))] = pieces[piecessss].name
                                    pieces[board[moveTo[0] + str(int(moveTo[1]))]].position = ["C" , pieces[board[moveTo[0] + str(int(moveTo[1]))]].position[1]]
                                    board["C" + str(int(pieces[board[moveTo[0] + str(int(moveTo[1]))]].position[1]))] = pieces[board[moveTo[0] + str(int(moveTo[1]))]].name
                                else:
                                    pieces[piecessss].position = ["G" , pieces[piecessss].position[1]]
                                    board["G" + str(int(pieces[piecessss].position[1]))] = pieces[piecessss].name
                                    pieces[board[moveTo[0] + str(int(moveTo[1]))]].position = ["F" , pieces[board[moveTo[0] + str(int(moveTo[1]))]].position[1]]
                                    board["F" + str(int(pieces[board[moveTo[0] + str(int(moveTo[1]))]].position[1]))] = pieces[board[moveTo[0] + str(int(moveTo[1]))]].name
                                board[moveTo[0] + str(int(moveTo[1]))] = ""
                                turn += 1
                            elif pieces[piecessss].follow:
                                pieces[piecessss].follow = False
                        elif pieces[piecessss].follow:
                            pieces[piecessss].follow = False
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
        else:
            if event.type == pygame.MOUSEBUTTONUP:
                promotionPiece = 0
                for y in range(2):
                    for x in range(2):
                        xEven = x % 2 == 0
                        yEven = y % 2 == 0
                        if promotion[1] == 1:
                            if squareSize//2*(x+1) + squareSize//2*x + squareSize*newX <= mouseXY[0] <= squareSize//2*(x+1) + squareSize//2*x + squareSize*newX + squareSize and squareSize//2*(y+1) + squareSize//2*y <= mouseXY[1] <= squareSize//2*(y+1) + squareSize//2*y + squareSize:
                                pieces[promotion[2] + promotionPieceTypes[promotionPiece] + numberOf(promotion[2] + promotionPieceTypes[promotionPiece], pieces.keys())] = piece(promotion[2], promotionPieceTypes[promotionPiece], [promotion[0], promotion[1]], promotion[2] + promotionPieceTypes[promotionPiece] + numberOf(promotion[2] + promotionPieceTypes[promotionPiece], pieces.keys()))
                                promotion = ""
                                break
                        else:
                            if squareSize//2*(x+1) + squareSize//2*x + squareSize*newX <= mouseXY[0] <= squareSize//2*(x+1) + squareSize//2*x + squareSize*newX and SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)* squareSize <= mouseXY[1] <= SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)* squareSize + squareSize:
                                pieces[promotion[2] + promotionPieceTypes[promotionPiece] + numberOf(promotion[2] + promotionPieceTypes[promotionPiece], pieces.keys())] = piece(promotion[2], promotionPieceTypes[promotionPiece], [promotion[0], promotion[1]], promotion[2] + promotionPieceTypes[promotionPiece] + numberOf(promotion[2] + promotionPieceTypes[promotionPiece], pieces.keys()))
                                promotion = ""
                                break
                        promotionPiece += 1
                    break

    # updates the frames of the game
    pygame.display.update()
  
pygame.quit()