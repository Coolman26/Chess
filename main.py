import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame

# initializing the constructor
pygame.init()

# shorthand events
def imgload(img): return pygame.image.load(img)

class piece():
    def __init__(self, color, type, position, name, follow=False) -> None:
        self.position = position
        self.color = color
        self.type = type
        self.png = loadpiece(color + type)
        self.follow = follow
        self.name = name
        board[position[0] + str(position[1])] = name
        if type == "pawn":
            self.movedTwo = False


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

def loadpiece(name):
    start = startscolor(name)
    end = endspiece(name)
    if start[0] and end[0]:
        piece = imgload("assets/GamePieces/" + start[1] + end[1] + ".png")
        piece = pygame.transform.smoothscale(piece, [squareSize-10, SCREEN_DIMENSIONS[1]/boardSize-20])
        return piece
def pieceInBetween(piece, moveTo):
    moveX = (boardSize - alphabet.index(pieces[piece].position[0])) - (boardSize - alphabet.index(moveTo[0]))
    moveY = int(pieces[piece].position[1] - moveTo[1])
    if moveX == 0:
        for i in range(-1 if moveY > 0 else 1, moveY*-1, -1 if moveY > 0 else 1):
            if board[pieces[piece].position[0] + str(int(pieces[piece].position[1] + i))] != "":
                return True
    elif moveY == 0:
        for i in range(-1 if moveX > 0 else 1, moveX*-1, -1 if moveX > 0 else 1):
            if board[alphabet[alphabet.index(pieces[piece].position[0]) - i] + str(int(pieces[piece].position[1]))] != "":
                return True
    else:
        for x in range(-1 if moveX > 0 else 1, moveX*-1, -1 if moveX > 0 else 1):
            for y in range(-1 if moveY > 0 else 1, moveY*-1, -1 if moveY > 0 else 1):
                if board[alphabet[alphabet.index(pieces[piece].position[0]) - x] + str(int(pieces[piece].position[1] + y))] != "" and abs(x) == abs(y):
                    return True
    return False


def canMove(piece, moveTo, board):
    global alphabet, boardSize, pieces, overRideCanMove, bottomColor
    moveX = (boardSize - alphabet.index(pieces[piece].position[0])) - (boardSize - alphabet.index(moveTo[0]))
    moveY = pieces[piece].position[1] - moveTo[1]
    color = pieces[piece].color
    type = pieces[piece].type
    if not overRideCanMove:
        if type == "bishop":
            if abs(moveX) == abs(moveY) and not pieceInBetween(piece, moveTo):
                return True

        elif type == "pawn":
            if abs(moveX) == 1 and abs(moveY) == 1 and board[moveTo[0] + str(int(moveTo[1]))] != "":
                return True
            elif abs(moveX) == 1 and abs(moveY) == 1 and 2 <= moveTo[1] <= 8 and int(moveTo[1]) + (1 if color == bottomColor else -1) < boardSize and "pawn" in board[moveTo[0] + str(int(moveTo[1]) + (1 if color == bottomColor else -1))]:
                if pieces[board[moveTo[0] + str(int(moveTo[1]) + (1 if color == bottomColor else -1))]].movedTwo != False:
                    return True
            else:
                if moveY in (([1, 2] if pieces[piece].position[1] == 7 else [1]) if color == bottomColor else ([-1, -2] if pieces[piece].position[1] == 2 else [-1])) and moveX == 0 and board[moveTo[0] + str(int(moveTo[1]))] == ""  and not pieceInBetween(piece, moveTo):
                    return True

        elif type == "king":
            moveX = abs(moveX) in [1, 0]
            moveY = abs(moveY) in [1, 0]
            if moveY and moveX:
                return True

        
        elif type == "queen":
            if abs(moveX) == abs(moveY) and not pieceInBetween(piece, moveTo):
                return True
            elif ((moveX == 0 and moveY != 0) or (moveY == 0 and moveX != 0)) and not pieceInBetween(piece, moveTo):
                return True
        
        elif type == "rook":
            if ((moveX == 0 and moveY != 0) or (moveY == 0 and moveX != 0)) and not pieceInBetween(piece, moveTo):
                return True

        elif type == "knight":
            if (abs(moveX) == 1 and abs(moveY) == 2) or (abs(moveY) == 1 and abs(moveX) == 2):
                return True
    else:
        return True

def inCheck(pieces, board):
    if not overRideCanMove:
        for Piece in pieces:
            if Piece != None and pieces[Piece] != "":
                color = pieces[Piece].color
                kingPosition = pieces[(bottomColor if color == topColor else topColor) + "king0"].position
                if canMove(Piece, kingPosition, board):
                    return bottomColor if color == topColor else topColor
    else:
        return None


        
def numberOf(key, list):
    x = 0
    for thing in list:
        if thing.startswith(key):
            x += 1
    return str(x)

def inTie():
    movePositions = {topColor:[], bottomColor:[]}
    for x in range(boardSize):
        for y in range(1, boardSize+1):
            for Piece in pieces:
                if Piece != None and pieces[Piece] != "" and canMove(Piece, [alphabet[x], y], board) and pieces[Piece].position != [alphabet[x], y]:
                    board1 = board.copy()
                    pieces1 = pieces.copy()
                    firstLocation = pieces1[Piece].position
                    board1[pieces1[Piece].position[0] + str(int(pieces1[Piece].position[1]))] = ""
                    pieces1[Piece].position = [alphabet[x], y]
                    board1[alphabet[x] + str(int(y))] = pieces1[Piece].name
                    checkState = inCheck(pieces1, board1)
                    if checkState == pieces1[Piece].color:
                        movePositions[pieces1[Piece].color].append(False)
                    else:
                        movePositions[pieces1[Piece].color].append(True)
                    pieces1[Piece].position = firstLocation
                    board1[pieces1[Piece].position[0] + str(int(pieces1[Piece].position[1]))] = pieces1[Piece].name
                    board1[alphabet[x] + str(int(y))] = ""
    for color in movePositions:
        if not True in movePositions[color]:
            return True
    if bottomColorCheckCounter == 3 or topColorCheckCounter == 3:
        return True
    return False
        
def canCastle(piece, moveTo):
    if pieces[piece].type == "king" and pieces[board[moveTo[0] + str(int(moveTo[1]))]].type == "rook" and not pieceInBetween(piece, moveTo):
        if pieces[piece].position[0] == "D" and pieces[piece].position[1] == (1 if pieces[piece].color == topColor else 8):
            if moveTo[0] in ["A", "H"] and moveTo[1] == (1 if pieces[piece].color == topColor else 8):
                return True

# screen resolution
SCREEN_DIMENSIONS = [800, 800]
developer = True
# bg = imgload("assets/other/backdrop.png")
# bg = pygame.transform.scale(bg, SCREEN_DIMENSIONS)
# logo = imgload("assets/other/logo.png")
# logo = pygame.transform.scale(logo, [390, 130])
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
height, width = screen.get_height(), screen.get_width()
pygame.display.set_caption("Chess")
icon = imgload("assets/icon.png")
pygame.display.set_icon(icon)
boardSize = 8
topColor = "black"
bottomColor = "white"
turn = 1
winner = ""
winnerLogo = imgload("assets/EndingPictures/Winner.jpg")
winnerLogo = pygame.transform.smoothscale(winnerLogo, [SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]//2])
loserLogo = imgload("assets/EndingPictures/Loser.jpg")
loserLogo = pygame.transform.smoothscale(loserLogo, [SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]//2])
tieLogo = imgload("assets/EndingPictures/Tie.jpg")
tieLogo = pygame.transform.smoothscale(tieLogo, [SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]])
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
promotionPieces = {}
promotionPieceTypes = ["bishop", "rook", "knight", "queen"]
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


# smallfont = pygame.font.SysFont('Corbel', 35)
# smallerfont = pygame.font.SysFont('Corbel', 32)

board = {}
for x in range(boardSize):
    for y in range(boardSize):
        board[alphabet[x] + str(y+1)] = ""
squareSize = SCREEN_DIMENSIONS[0]/boardSize
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
topColorCheckCounter = 0
bottomColorCheckCounter = 0


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
    print(topColorCheckCounter, bottomColorCheckCounter)
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

            
    # stores the (x,y) coordinates into
    # the variable as a tuple
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
    # screen.blit(logo, (93, 50))
    
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
                        if pieces[piecessss].follow and not pieces[piecessss].position == moveTo and canMove(piecessss, moveTo, board):
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
                                checkState = inCheck(pieces, board)
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
                                checkState = inCheck(pieces, board)
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
                            if canCastle(piecessss, moveTo):
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