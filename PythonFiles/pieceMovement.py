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
    boardSize = vars["boardSize"]
    overRideCanMove = vars["overRideCanMove"]
    moveX = alphabet.index(pieces[piece].position[0]) - alphabet.index(moveTo[0])
    moveY = pieces[piece].position[1] - moveTo[1]
    type = pieces[piece].type
    name = pieces[piece].name
    topColor = vars["topColor"]
    color = pieces[piece].color
    if not overRideCanMove:
        # if type != "pawn":
        #     print("HIII")
        #     if board[moveTo[0] + str(int(moveTo[1]))] == "" or pieces[board[moveTo[0] + str(int(moveTo[1]))]].color != pieces[piece].color:
        #         if type == "bishop":
        #             if abs(moveX) == abs(moveY) and not pieceInBetween(piece, moveTo, vars):
        #                 return True

        #         elif type == "pawn":
        #             if moveX == 0 and moveY == 1 and board[moveTo[0] + str(int(moveTo[1]))] == "":
        #                 return True
        #             elif abs(moveX) == 1 and moveY == 1:
        #                 if board[moveTo[0] + str(int(moveTo[1]))] != "":
        #                     return True
        #                 elif abs(moveX) == 1 and moveY == 1 and 2 <= moveTo[1] <= 8 and int(moveTo[1]) + 1 < boardSize and "pawn" in board[moveTo[0] + str(int(moveTo[1])+1)]:
        #                     if pieces[board[moveTo[0] + str(int(moveTo[1]) + 1)]].movedTwo != False:
        #                         return True
        #             else:
        #                 if (moveY == 2 and moveX == 0 and board[moveTo[0] + str(int(moveTo[1]))] == ""  and not pieceInBetween(piece, moveTo, vars)) and (pawnCanTake(piece, vars)):
        #                     return True

        #         elif type == "king":
        #             moveX = abs(moveX) in [1, 0]
        #             moveY = abs(moveY) in [1, 0]
        #             if moveY and moveX:
        #                 return True

                
        #         elif type == "queen":
        #             if abs(moveX) == abs(moveY) and not pieceInBetween(piece, moveTo, vars):
        #                 return True
        #             elif ((moveX == 0 and moveY != 0) or (moveY == 0 and moveX != 0)) and not pieceInBetween(piece, moveTo, vars):
        #                 return True
                
        #         elif type == "rook":
        #             if ((moveX == 0 and moveY != 0) or (moveY == 0 and moveX != 0)) and not pieceInBetween(piece, moveTo, vars):
        #                 return True

        #         elif type == "knight":
        #             if (abs(moveX) == 1 and abs(moveY) == 2) or (abs(moveY) == 1 and abs(moveX) == 2):
        #                 return True
        #         elif canCastle(piece, moveTo, vars):
        #             return True
        # else:
            movementTypes = vars["settings"][type]
            ogRow = "row" + str(pieces[piece].position[1] if color != topColor else boardSize-pieces[piece].position[1]+1)
            ogCol = alphabet.index(pieces[piece].position[0]) if color != topColor else boardSize-alphabet.index(pieces[piece].position[0])-1
            for movementType in movementTypes:
                if moveX == 0 and moveY != 0:
                    if "up" in movementType:
                        if movementType == "up":
                            if moveY > 0:
                                if not pieceInBetween(piece, moveTo, vars):
                                    return True
                        elif len(movementType.split()) == 1:
                            print(int(movementType[2]) == moveY)
                            if int(movementType[2]) == moveY:
                                if not pieceInBetween(piece, moveTo, vars):
                                    return True
                        elif len(movementType.split()) == 2:
                            if int(movementType[2]) == moveY:
                                if movementType.split()[1] == "first":
                                    if vars["settings"][ogRow][ogCol] == ("top" if color == topColor else "bottom") + type:
                                        if not pieceInBetween(piece, moveTo, vars):
                                            return True
                    elif "down" in movementType:
                        if movementType == "down":
                            if moveY < 0:
                                if not pieceInBetween(piece, moveTo, vars):
                                    return True
                        elif len(movementType.split()) == 1:
                            if movementType[2]*-1 == moveY:
                                if not pieceInBetween(piece, moveTo, vars):
                                    return True
                        elif len(movementType.split()) == 2:
                            if movementType[2]*-1 == moveY:
                                if movementType.split()[1] == "first":
                                    if vars["settings"][ogRow][ogCol] == ("top" if color == topColor else "bottom") + type:
                                        if not pieceInBetween(piece, moveTo, vars):
                                            return True
                elif moveX != 0 and moveY != 0:
                    if movementType == "en passant":
                        if abs(moveX) == 1 and moveY == 1 and 2 <= moveTo[1] <= 8 and int(moveTo[1]) + 1 < boardSize and type in board[moveTo[0] + str(int(moveTo[1])+1)]:
                            if pieces[board[moveTo[0] + str(int(moveTo[1]) + 1)]].movedTwo != False:
                                if not pieceInBetween(piece, moveTo, vars):
                                    return True
                    elif "diagonal" in movementType:
                        if len(movementType.split()) == 3:
                            if moveX == int(movementType.split()[1]) and moveY == int(movementType.split()[1]):
                                if movementType.split()[2] == "take":
                                    if board[moveTo[0] + str(int(moveTo[1]))] != "":
                                        if not pieceInBetween(piece, moveTo, vars):
                                            return True
                        elif abs(moveX) == abs(moveY) and not pieceInBetween(piece, moveTo, vars):
                            return True
                    elif "L" in movementType:
                        if (abs(moveX) == 1 and abs(moveY) == 2) or (abs(moveY) == 1 and abs(moveX) == 2):
                            return True
                        
                
                elif moveX != 0 and moveY == 0:
                    if "left" in movementType:
                        if movementType == "left":
                            if moveX < 0:
                                return True
                        elif len(movementType.split()) == 1:
                            if int(movementType[-1]) == moveX:
                                return True
                        elif len(movementType.split()) == 2:
                            if int(movementType.split()[0][-1]) == moveX:
                                if movementType.split()[1] == "first":
                                    if vars["settings"][ogRow][ogCol] == ("top" if color == topColor else "bottom") + type:
                                        if not pieceInBetween(piece, moveTo, vars):
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
    