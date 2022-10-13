from PythonFiles.pieceMovement import canMove

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def inTie(board, pieces, boardSize, bottomColor, overRideCanMove, topColor):
    movePositions = {topColor:[], bottomColor:[]}
    for x in range(boardSize):
        for y in range(1, boardSize+1):
            for Piece in pieces:
                if Piece != None and pieces[Piece] != "" and canMove(Piece, [alphabet[x], y], board, pieces, boardSize, bottomColor, overRideCanMove) and pieces[Piece].position != [alphabet[x], y]:
                    board1 = board.copy()
                    pieces1 = pieces.copy()
                    firstLocation = pieces1[Piece].position
                    board1[pieces1[Piece].position[0] + str(int(pieces1[Piece].position[1]))] = ""
                    pieces1[Piece].position = [alphabet[x], y]
                    board1[alphabet[x] + str(int(y))] = pieces1[Piece].name
                    checkState = inCheck(pieces1, board1, overRideCanMove, bottomColor, topColor, boardSize)
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

def inCheck(pieces, board, overRideCanMove, bottomColor, topColor, boardSize):
    if not overRideCanMove:
        for Piece in pieces:
            if Piece != None and pieces[Piece] != "":
                color = pieces[Piece].color
                kingPosition = pieces[(bottomColor if color == topColor else topColor) + "king0"].position
                if canMove(Piece, kingPosition, board, pieces, boardSize, bottomColor, overRideCanMove, topColor):
                    return bottomColor if color == topColor else topColor
    else:
        return None