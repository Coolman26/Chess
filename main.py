import json
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from PythonFiles.pieceMovement import canCastle, canMove, castle, nextTurn
from PythonFiles.pieceCreation import imgload, numberOf, Piece
from PythonFiles.chessGameStates import inCheck, inTie
from PythonFiles.promotion import promotionBoard



# Initializing the constructor
pygame.init()

# Used to plug the global variables into the other py's
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
        "promotionPieces": promotionPieces,
        "turn": turn,
        "promotionPieceTypes": promotionPieceTypes
    }

# Resets the global variables
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
    turn = [1]
    winner = ""
    for x in range(boardSize):
        for y in range(boardSize):
            board[alphabet[x] + str(y+1)] = ""

    pieces = {}
    for i in range(boardSize):
        for piece in range(len(settings["row" + str(i+1)])):
            PieceName = settings["row" + str(i+1)][::-1][piece]
            if PieceName != "":
                PieceType = PieceName[3:] if PieceName.startswith(
                    "top") else PieceName[6:]
                PieceColor = topColor if PieceName.startswith(
                    "top") else bottomColor
                PieceName = PieceColor + PieceType + \
                    numberOf(PieceColor + PieceType, pieces.keys())
                pieces[PieceName] = Piece(PieceColor, PieceType, [alphabet[piece], i+1], PieceName, globalVariables())

    


# Base Settings of the Game
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
    mouseXY = pygame.mouse.get_pos() 
    mousePressed = pygame.mouse.get_pressed()

    if delete and delete[0] != "":  # This deletes a piece in pieces if the delete list has something in it.
        del pieces[delete[0]]
        delete = []

    # This changes any pawn that has movedTwo equal to True(which means they have moved two spaces) to equal False if it has been more than one turn.
    for piece in pieces:
        if pieces[piece].type == "pawn":
            if pieces[piece].movedTwo != False:
                if turn[0] - 1 == pieces[piece].movedTwo[1]:
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

    eventGet = pygame.event.get()
    if promotion != "":
        promotion = promotionBoard(globalVariables(), eventGet, mouseXY)
    for event in eventGet:

        if event.type == pygame.QUIT:
            running = False

        if promotion == "":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not removePiece:
                    # Picks up a piece
                    for piece in pieces:
                        if (turn[0] % 2 == 0 if pieces[piece].color == topColor else turn[0] % 2 == 1) or overRideTurns:
                            if mouseXY[0] // squareSize + 1 == (boardSize - alphabet.index(pieces[piece].position[0])) and mouseXY[1] // squareSize + 1 == pieces[piece].position[1]:
                                pieces[piece].follow = True
                else:
                    # Removes a piece if that mode is on
                    if not board[alphabet[int(boardSize - mouseXY[0] // squareSize - 1)] + str(int(mouseXY[1] // squareSize + 1))] == "":
                        del pieces[board[alphabet[int(
                            boardSize - mouseXY[0] // squareSize - 1)] + str(int(mouseXY[1] // squareSize + 1))]]
                        board[alphabet[int(boardSize - mouseXY[0] // squareSize - 1)] +
                              str(int(mouseXY[1] // squareSize + 1))] = ""
            elif event.type == pygame.MOUSEBUTTONUP:
                for piece in pieces:
                    # Finds the coords of where a piece was dropped
                    moveTo = [alphabet[int(
                        boardSize - mouseXY[0] // squareSize - 1)], mouseXY[1] // squareSize + 1]
                    if pieces[piece].follow and not pieces[piece].position == moveTo and canMove(piece, moveTo, globalVariables()):
                        # Saves the original location of the piece
                        firstLocation = pieces[piece].position
                        pieces[piece].follow = False

                        if canCastle(piece, moveTo, globalVariables()):
                            castle(piece, moveTo, globalVariables())
                        
                        # How it moves the piece and what to do if the new position isn't empty
                        else:
                            board[pieces[piece].position[0] +
                                  str(int(pieces[piece].position[1]))] = ""
                            print(board[moveTo[0] + str(int(moveTo[1]))])
                            if board[moveTo[0] + str(int(moveTo[1]))] != "":
                                delete = [board[moveTo[0] + str(int(moveTo[1]))]]
                                print(delete)
                                if pieces[board[moveTo[0] + str(int(moveTo[1]))]].type == "king":
                                    winner = pieces[board[moveTo[0] + str(int(moveTo[1]))]].color
                                    break
                            board[moveTo[0] + str(int(moveTo[1]))] = pieces[piece].name
                            pieces[piece].moveTo(moveTo) 
                            

                        # Deals with Check
                        checkState = inCheck(globalVariables())
                        # Resets the piece if it makes their king get into check because of the movement
                        if (checkState != None and check != None) or (checkState == pieces[piece].color):
                            pieces[piece].moveTo(firstLocation)
                            board[pieces[piece].position[0] +
                                  str(int(pieces[piece].position[1]))] = pieces[piece].name
                            board[moveTo[0] + str(int(moveTo[1]))] = ""
                            break
                        # Declares check if the board is in check
                        elif checkState != None:
                            check = checkState
                        # Resets check if need be
                        elif checkState == None and check != None:
                            check = None
                        
                        # Extra pawn functions
                        if pieces[piece].type == "pawn":
                            # Activates promotion
                            if pieces[piece].position[1] == 1:
                                promotion = pieces[piece].position + \
                                    [pieces[piece].color]

                            # Makes the pawn have movedTwo equal to true if it movedTwo(used for Au Passant)
                            if abs(firstLocation[1] - int(moveTo[1])) == 2:
                                pieces[piece].movedTwo = [True, turn[0]+1]
                            # Deletes the pawn that got Au Passant-ed
                            if abs(alphabet.index(firstLocation[0]) - alphabet.index(moveTo[0])) == 1 and board[moveTo[0] + str(int(moveTo[1]))] == pieces[piece].name:
                                delete = [board[moveTo[0] + str(int(moveTo[1])+ 1)]]
                                board[moveTo[0] + str(int(moveTo[1])-1)] = ""
                        
                        if promotion == "": 
                            nextTurn(globalVariables())
                        break
                    else:
                        pieces[piece].follow = False
                        
            # Developer Controls(activated by the left control if developer is True)
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
    
            

    # Updates the frames of the game
    pygame.display.update()

pygame.quit()
