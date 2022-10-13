alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def pieceInBetween(piece, moveTo, board, pieces, boardSize):
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


def canMove(piece, moveTo, board, pieces, boardSize, bottomColor, overRideCanMove):
    moveX = (boardSize - alphabet.index(pieces[piece].position[0])) - (boardSize - alphabet.index(moveTo[0]))
    moveY = pieces[piece].position[1] - moveTo[1]
    color = pieces[piece].color
    type = pieces[piece].type
    if not overRideCanMove:
        if type == "bishop":
            if abs(moveX) == abs(moveY) and not pieceInBetween(piece, moveTo, board, pieces, boardSize):
                return True

        elif type == "pawn":
            if abs(moveX) == 1 and abs(moveY) == 1 and board[moveTo[0] + str(int(moveTo[1]))] != "":
                return True
            elif abs(moveX) == 1 and abs(moveY) == 1 and 2 <= moveTo[1] <= 8 and int(moveTo[1]) + (1 if color == bottomColor else -1) < boardSize and "pawn" in board[moveTo[0] + str(int(moveTo[1]) + (1 if color == bottomColor else -1))]:
                if pieces[board[moveTo[0] + str(int(moveTo[1]) + (1 if color == bottomColor else -1))]].movedTwo != False:
                    return True
            else:
                if moveY in (([1, 2] if pieces[piece].position[1] == 7 else [1]) if color == bottomColor else ([-1, -2] if pieces[piece].position[1] == 2 else [-1])) and moveX == 0 and board[moveTo[0] + str(int(moveTo[1]))] == ""  and not pieceInBetween(piece, moveTo, board, pieces, boardSize):
                    return True

        elif type == "king":
            moveX = abs(moveX) in [1, 0]
            moveY = abs(moveY) in [1, 0]
            if moveY and moveX:
                return True

        
        elif type == "queen":
            if abs(moveX) == abs(moveY) and not pieceInBetween(piece, moveTo, board, pieces, boardSize):
                return True
            elif ((moveX == 0 and moveY != 0) or (moveY == 0 and moveX != 0)) and not pieceInBetween(piece, moveTo, board, pieces, boardSize):
                return True
        
        elif type == "rook":
            if ((moveX == 0 and moveY != 0) or (moveY == 0 and moveX != 0)) and not pieceInBetween(piece, moveTo, board, pieces, boardSize):
                return True

        elif type == "knight":
            if (abs(moveX) == 1 and abs(moveY) == 2) or (abs(moveY) == 1 and abs(moveX) == 2):
                return True
        
        elif 
    else:
        return True

def canCastle(piece, moveTo, board, topColor, pieces, boardSize):
    if pieces[piece].type == "king" and pieces[board[moveTo[0] + str(int(moveTo[1]))]].type == "rook" and not pieceInBetween(piece, moveTo, board, pieces, boardSize):
        if pieces[piece].position[0] == "D" and pieces[piece].position[1] == (1 if pieces[piece].color == topColor else 8):
            if moveTo[0] in ["A", "H"] and moveTo[1] == (1 if pieces[piece].color == topColor else 8):
                return True