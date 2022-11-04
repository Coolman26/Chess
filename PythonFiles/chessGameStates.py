from PythonFiles.pieceMovement import canMove

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def inTie(vars):
    movePositions = {vars["topColor"]:[], vars["bottomColor"]:[]}
    for x in range(vars["boardSize"]):
        for y in range(1, vars["boardSize"]+1):
            for Piece in vars["pieces"]:
                if Piece != None and vars["pieces"][Piece] != "" and canMove(Piece, [alphabet[x], y], vars) and vars["pieces"][Piece].position != [alphabet[x], y]:
                    board1 = vars["board"].copy()
                    pieces1 = vars["pieces"].copy()
                    firstLocation = pieces1[Piece].position
                    board1[pieces1[Piece].position[0] + str(int(pieces1[Piece].position[1]))] = ""
                    pieces1[Piece].position = [alphabet[x], y]
                    board1[alphabet[x] + str(int(y))] = pieces1[Piece].name
                    checkState = inCheck(pieces1, board1, vars)
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

def inCheck(vars):
    if not vars["overRideCanMove"]:
        for Piece in vars["pieces"]:
            if Piece != None and vars["pieces"][Piece] != "":
                color = vars["pieces"][Piece].color
                kingPosition = vars["pieces"][(vars["bottomColor"] if color == vars["topColor"] else vars["topColor"]) + "king0"].position
                if canMove(Piece, kingPosition, vars):
                    return vars["bottomColor"] if color == vars["topColor"] else vars["topColor"]
    else:
        return None