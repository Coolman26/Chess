import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame, json

from PythonFiles.chessGameStates import inCheck, inTie
from PythonFiles.pieceCreation import imgload, loadpiece, numberOf
from PythonFiles.pieceMovement import canCastle, canMove

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

def nextTurn():
    global turn, board, pieces
    turn += 1
    for x in range(boardSize):
        for y in range(boardSize):
            board[alphabet[x] + str(y+1)] = ""
    for Piece in pieces:
        if pieces[Piece] != "":
            pieces[Piece].position = [alphabet[7 - alphabet.index(pieces[Piece].position[0])], 9 - pieces[Piece].position[1]]
            board[pieces[Piece].position[0] + str(int(pieces[Piece].position[1]))] = Piece

## Base Variables of Game
settings = json.load(open('profile.json'))
SCREEN_DIMENSIONS = [800, 800] # How wide the screen is by how tall the screen is in pixels
developer = True # Whether or not you can hit left control to access developer commands
boardSize = settings["boardSize"] # How many squares for the length and width
topColor = settings["topColor"] # Which color starts on the top of the board
bottomColor = settings["bottomColor"] # Which color starts at the bottom of the board and goes first
promotionPieceTypes = ["bishop", "rook", "knight", "queen"] # Which pieces are available when a pawn is being promoted(must have a png to back it up)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # The alphabet which the game uses
squareSize = SCREEN_DIMENSIONS[0]/boardSize # How large each square is



## Setting the screen up
screen = pygame.display.set_mode(SCREEN_DIMENSIONS) #Creating the screen with the dimensions established earlier #
pygame.display.set_caption("Chess") #Setting the title for the game
icon = imgload("assets/icon.png") #Loading in the icon for the game
pygame.display.set_icon(icon) #Setting the icon loaded in as the icon of the screen

## Importing logos
winnerLogo = imgload("assets/EndingPictures/Winner.jpg") #Loads in the logo
winnerLogo = pygame.transform.smoothscale(winnerLogo, [SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]//2]) #Transforms the logo to the correct size(height is half)
loserLogo = imgload("assets/EndingPictures/Loser.jpg") #Loads in the logo
loserLogo = pygame.transform.smoothscale(loserLogo, [SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]//2]) #Transforms the logo to the correct size(height is half)
tieLogo = imgload("assets/EndingPictures/Tie.jpg") #Loads in the logo
tieLogo = pygame.transform.smoothscale(tieLogo, [SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]]) #Transforms the logo to the correct size

## Importing Promotion Pieces
# Using the promotionPieceTypes variable from earlier it goes through for each color and type and imports and scales each image correctly.
# This is to be later used for promotion. 

promotionPieces = {}
for x in range(2):
    for y in range(len(promotionPieceTypes)):
        Piece = imgload("assets/GamePieces/" + (topColor if x == 1 else bottomColor).capitalize() + promotionPieceTypes[y].capitalize() + ".png")
        promotionPieces[(topColor if x == 1 else bottomColor) + str(y)] = pygame.transform.smoothscale(Piece, [squareSize-10, SCREEN_DIMENSIONS[1]/boardSize-20])

# Tile Colors
tileColor1 = settings["tileColor1"]
tileColor2 = settings["tileColor2"]

#This function resets all of the variables back to their starting position. MUST NOT BE MOVED.
def reset():
    global board, pieces, delete, check, tie, overRideCanMove, removePiece, overRideTurns, promotion, turn, winner
    board = {}
    for x in range(boardSize):
        for y in range(boardSize):
            board[alphabet[x] + str(y+1)] = ""

    pieces = {}
    for i in range(boardSize):
        for Piece in range(len(settings["Row" + str(i+1)])):
            PieceName = settings["Row" + str(i+1)][Piece]
            if PieceName != "":
                PieceType = PieceName[3:] if PieceName.startswith("top") else PieceName[6:]
                PieceColor = topColor if PieceName.startswith("top") else bottomColor
                PieceName = PieceColor + PieceType + numberOf(PieceColor + PieceType, pieces.keys())
                pieces[PieceName] = piece(PieceColor, PieceType, [alphabet[Piece], i+1], PieceName)

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
    mouseXY = pygame.mouse.get_pos() #This gets the current mouse position
    mouse = pygame.mouse.get_pressed() #This gets the current mouse buttons that are pressed

    if delete: #This deletes a piece in pieces if the delete list has something in it. 
        # I did this because it activates inside of a for loop and I can't delete inside the for loop.
        del pieces[delete[0]]
        delete = []
    
    #This changes any pawn that has movedTwo equal to True(which means they have moved two spaces) to equal False if it has been more than one turn.
    for Piece in pieces:
        if pieces[Piece].type == "pawn":
            if pieces[Piece].movedTwo != False:
                if turn - 1 == pieces[Piece].movedTwo[1]:
                    pieces[Piece].movedTwo = False
    
    if not removePiece and promotion != "": # This checks if the game is inTie if it is then it checks if one side is in check. 
    # If they are in check then it is a checkmate and it ends.
        if inTie(board, pieces, boardSize, bottomColor, overRideCanMove, topColor):
            if check != None:
                winner = check
            else:
                tie = True

    #Loads the board tiles
    for y in range(boardSize):
        for x in range(boardSize):
            xEven = x % 2 == 0
            yEven = y % 2 == 0
            if (xEven and yEven) or (not xEven and not yEven): 
                pygame.draw.rect(screen, tileColor2, [squareSize*(x), squareSize*(y), squareSize*(x+1), squareSize*(y+1)])
            else: 
                pygame.draw.rect(screen, tileColor1, [squareSize*(x), squareSize*(y), squareSize*(x+1), squareSize*(y+1)])

    for activePiece in pieces:
        if not pieces[activePiece].follow:
            x = boardSize - alphabet.index(pieces[activePiece].position[0])
            y = pieces[activePiece].position[1]
            screen.blit(pieces[activePiece].png, [10+((x-1)*squareSize), (y-1)*(SCREEN_DIMENSIONS[1]/boardSize)+10])
        else:
            screen.blit(pieces[activePiece].png, [mouseXY[0]-(squareSize/3), mouseXY[1]-(SCREEN_DIMENSIONS[1]/boardSize/3) ])

    if promotion != "":
        promotionPiece = 0
        newX = boardSize - alphabet.index(promotion[0]) - (1 if alphabet.index(promotion[0]) != 0 else 3)
        for y in range(2):
            for x in range(2):
                xEven = x % 2 == 0
                yEven = y % 2 == 0
                if promotion[1] == 1:
                    if (xEven and yEven) or (not xEven and not yEven): 
                        pygame.draw.rect(screen, tileColor2, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, squareSize//2*(y+1) + squareSize//2*y, squareSize, squareSize])
                    else: 
                        pygame.draw.rect(screen, tileColor1, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, squareSize//2*(y+1) + squareSize//2*y, squareSize, squareSize])
                    screen.blit(promotionPieces[promotion[2] + str(promotionPiece)], [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX + 10, squareSize//2*(y+1) + squareSize//2*y + 10])
                else:
                    if (xEven and yEven) or (not xEven and not yEven): 
                        pygame.draw.rect(screen, tileColor2, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)* squareSize, squareSize, squareSize])
                    else: 
                        pygame.draw.rect(screen, tileColor1, [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX, SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)*squareSize, squareSize, squareSize])
                    screen.blit(promotionPieces[promotion[2] + str(promotionPiece)], [squareSize//2*(x+1) + squareSize//2*x + squareSize*newX + 10, SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)*squareSize + 10])
                promotionPiece += 1

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
                for piecessss in pieces:
                    moveTo = [alphabet[int(boardSize - mouseXY[0] // squareSize - 1)], mouseXY[1] // squareSize + 1]
                    if pieces[piecessss].follow and not pieces[piecessss].position == moveTo and canMove(piecessss, moveTo, board, pieces, boardSize, bottomColor, overRideCanMove, topColor):
                        if check == None:
                            if turn % 2 == 1:
                                bottomColorCheckCounter = 0
                            else:
                                topColorCheckCounter = 0
                        
                        firstLocation = pieces[piecessss].position
                        pieces[piecessss].follow = False
                        if pieces[piecessss].type == "pawn":
                            if pieces[piecessss].position[1] == (8 if pieces[piecessss].color == topColor else 1):
                                promotion = pieces[piecessss].position + [pieces[piecessss].color]
                            elif abs(firstLocation[1] - int(moveTo[1])) == 2:
                                pieces[piecessss].movedTwo = [True, turn+1]
                            elif abs(alphabet.index(firstLocation[0]) - alphabet.index(moveTo[0])) == 1 and board[moveTo[0] + str(int(moveTo[1]))] == "":
                                delete = [board[moveTo[0] + str(int(moveTo[1])+(1 if pieces[piecessss].color == bottomColor else -1))]]
                                board[moveTo[0] + str(int(moveTo[1])-1)] = ""
                        if not board[moveTo[0] + str(int(moveTo[1]))] == "":
                            board[pieces[piecessss].position[0] + str(int(pieces[piecessss].position[1]))] = ""
                            delete = [board[moveTo[0] + str(int(moveTo[1]))]]
                            if pieces[board[moveTo[0] + str(int(moveTo[1]))]].type == "king":
                                winner = pieces[board[moveTo[0] + str(int(moveTo[1]))]].color
                                break
                            pieces[board[moveTo[0] + str(int(moveTo[1]))]] = ""
                            pieces[piecessss].position = moveTo
                        elif canCastle(piecessss, moveTo, board, topColor, pieces, boardSize):
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
                        else:
                            board[pieces[piecessss].position[0] + str(int(pieces[piecessss].position[1]))] = ""
                            pieces[piecessss].position = moveTo
                            board[moveTo[0] + str(int(moveTo[1]))] = pieces[piecessss].name
                        checkState = inCheck(pieces, board, overRideCanMove, bottomColor, topColor, boardSize)
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
                        nextTurn()
                        break
                    else:
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
                        pieceName = promotion[2] + promotionPieceTypes[promotionPiece] + numberOf(promotion[2] + promotionPieceTypes[promotionPiece], pieces.keys())
                        if promotion[1] == 1:
                            if squareSize//2*(x+1) + squareSize//2*x + squareSize*newX <= mouseXY[0] <= squareSize//2*(x+1) + squareSize//2*x + squareSize*newX + squareSize and squareSize//2*(y+1) + squareSize//2*y <= mouseXY[1] <= squareSize//2*(y+1) + squareSize//2*y + squareSize:
                                pieces[pieceName] = piece(promotion[2], promotionPieceTypes[promotionPiece], [promotion[0], promotion[1]], pieceName)
                                promotion = ""
                                break
                        else:
                            if squareSize//2*(x+1) + squareSize//2*x + squareSize*newX <= mouseXY[0] <= squareSize//2*(x+1) + squareSize//2*x + squareSize*newX and SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)* squareSize <= mouseXY[1] <= SCREEN_DIMENSIONS[1] - squareSize//2*(y+1) + squareSize//2*y - (y+1)* squareSize + squareSize:
                                pieces[pieceName] = piece(promotion[2], promotionPieceTypes[promotionPiece], [promotion[0], promotion[1]], pieceName)
                                promotion = ""
                                break
                        promotionPiece += 1
                    break

    # updates the frames of the game
    pygame.display.update()
  
pygame.quit()