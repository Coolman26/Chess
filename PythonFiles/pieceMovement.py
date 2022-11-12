import playsound
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def pieceInBetween(piece, moveTo, vars):
    pieces = vars["pieces"]
    board = vars["board"]
    boardSize = vars["boardSize"]
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


def canMove(piece, moveTo, vars):
    pieces = vars["pieces"]
    board = vars["board"]
    overRideCanMove = vars["overRideCanMove"]
    moveX = alphabet.index(pieces[piece].position[0]) - alphabet.index(moveTo[0])
    moveY = pieces[piece].position[1] - moveTo[1]
    type = pieces[piece].type
    if not overRideCanMove:
        movementTypes = vars["settings"][type]
        for movementType in movementTypes:
            move = movementType[0]
            if move in ["up", "down", "left", "right", "diagonal"] and pieceInBetween(piece, moveTo, vars):
                continue
            isAmtMovedCorrect = True
            isTurnCorrect = True
            canMoveToThatSpot = True
            if move == "up":
                isMovingInDirection = moveY > 0 and moveX == 0
            elif move == "down":
                isMovingInDirection = moveY < 0 and moveX == 0
            elif move == "left":
                isMovingInDirection = moveY == 0 and moveX < 0
            elif move == "right":
                isMovingInDirection = moveY == 0 and moveX > 0
            elif move == "diagonal":
                isMovingInDirection = moveY != 0 and moveX != 0 and abs(moveY) == abs(moveX)
            elif move == "L":
                isMovingInDirection = (abs(moveX) == 1 and abs(moveY) == 2) or (abs(moveY) == 1 and abs(moveX) == 2)
            elif move == "en passant":
                isMovingInDirection = moveY == 1 and abs(moveX) == 1 and type in board[moveTo[0] + str(int(moveTo[1])+1)]

            
            if movementType[1] != "":
                if move == "up":
                    isAmtMovedCorrect = int(movementType[1]) == moveY
                elif move == "down":
                    isAmtMovedCorrect = int(movementType[1])*-1 == moveY
                elif move == "left":
                    isAmtMovedCorrect = int(movementType[1]) == moveX
                elif move == "right":
                    isAmtMovedCorrect = movementType[1]*-1 == moveX
                elif move == "diagonal":
                    isAmtMovedCorrect = moveX == int(movementType[1]) and moveY == int(movementType[1])
                

            if movementType[2] != "":
                isTurnCorrect = int(movementType[2]) == pieces[piece].timesMoved+1
            
            if movementType[3] != "":
                if movementType[3] == "move":
                    canMoveToThatSpot = board[moveTo[0] + str(int(moveTo[1]))] == ""
                elif movementType[3] == "take":
                    canMoveToThatSpot = board[moveTo[0] + str(int(moveTo[1]))] == ""

            if not(isAmtMovedCorrect and isTurnCorrect and canMoveToThatSpot and isMovingInDirection):
                continue
            else:
                return True
        
    else:
        return True

def pawnCanTake(piece, vars):
    pieces = vars["pieces"]
    board = vars["board"]
    for x in [-1, 1]:
        if board[alphabet[alphabet.index(pieces[piece].position[0]) + x] + str(int(pieces[piece].position[1] + 1))] != "":
            return True
    


def canCastle(piece, moveTo, vars):
    pieces = vars["pieces"]
    board = vars["board"]
    if pieces[piece].type == "king" and board[moveTo[0] + str(int(moveTo[1]))] != "" and pieces[board[moveTo[0] + str(int(moveTo[1]))]].type == "rook" and not pieceInBetween(piece, moveTo, vars):
        if pieces[piece].position[0] == "D" and pieces[piece].position[1] == 8:
            if moveTo[0] in ["A", "H"] and moveTo[1] == 8:
                return True

def castle(piecessss, moveTo, vars):
    pieces = vars["pieces"]
    board = vars["board"]
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

def nextTurn(vars):
    boardSize = vars["boardSize"]
    board = vars["board"]
    pieces = vars["pieces"]
    turn = vars["turn"]
    turn[0] += 1
    for x in range(boardSize):
        for y in range(boardSize):
            board[alphabet[x] + str(y+1)] = ""
    for piece in pieces:
        if pieces[piece] != "":
            pieces[piece].position = [
                alphabet[7 - alphabet.index(pieces[piece].position[0])], 9 - pieces[piece].position[1]]
            board[pieces[piece].position[0] +
                  str(int(pieces[piece].position[1]))] = piece

def playSound(sound):
    if sound == "move":
        playsound.playsound("assets/SoundEffects/moveSound.mp3")
    elif sound == "take":
        playsound.playsound("assets/SoundEffects/takeSound.mp3")
    