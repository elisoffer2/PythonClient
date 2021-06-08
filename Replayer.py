import sys
import time
import OthelloClass

def ToArray(in_boardStr):
    OthelloObject = OthelloClass.Board()
    for i in range(0,len(in_boardStr)):
        if in_boardStr[i] == "0":
            OthelloObject.gameBoard[int(i/8)][i%8] = OthelloClass.spaceState.EMPTY
        elif in_boardStr[i] == "1":
            OthelloObject.gameBoard[int(i/8)][i%8] = OthelloClass.spaceState.BLACK
        elif in_boardStr[i] == "2":
            OthelloObject.gameBoard[int(i/8)][i%8] = OthelloClass.spaceState.WHITE
    return OthelloObject.gameBoard

def colorInt2Str(colorInt):
    if (colorInt == 0):
        return "Empty"
    elif (colorInt == 1):
        return "Black"
    elif (colorInt == 2):
        return "White"
    else:
        return "Error"

def main(argv):
    # construct the default board
    gameObject = OthelloClass.Board()
    currentLine = ""
    delimiter = ":"
    turnStr = ""
    colorStr = ""
    boardStr = ""
    parseCount = 0
    pos = 0

    if (len(argv) < 1):
        print(argv)
        print("missing input file name")
        return 1

    filename = argv[0]
    #GameLogs/eli_6db9d4ae-1a14-4850-a5f8-2282c32eed59.txt

    if (filename != ""):
        input_file = open(filename,"r")
        #cout << filename << endl;
        fileLines = input_file.read()
        fileLines = fileLines.split("\n")
        fileLines = fileLines[1:]
        # print(fileLines)
        
        for currentLine in fileLines:
            if currentLine == "":
                break
            splitLine = currentLine.split(":")
            colorStr = splitLine[0]
            boardStr = splitLine[1]
            turnStr = splitLine[2]

            # print(colorStr)
            # print(boardStr)
            # print(turnStr)

            print("Currently " + turnStr + " with the color " + colorInt2Str(int(colorStr)))
            
            gameObject.gameBoard = ToArray(boardStr)
            gameObject.display(gameObject.gameBoard,(gameObject.turn));
            response = input("")
    else:
        return 2

    return 0;

if __name__ == "__main__":
    main(sys.argv[1:])