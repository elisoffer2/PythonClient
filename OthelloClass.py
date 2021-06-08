from enum import Enum
from copy import copy
import math
import time
from datetime import datetime
import random

NOHEURVAL = 2147483645    # 2^31 -1
POSINF = 2147483646       # 2^31 - 2
RETOVERHEAD = 50          # overhead timing of return function in milliseconds
DEFAULT_TIME_PER_MOVE = 2 # Default timing of a move

moveTimeout = DEFAULT_TIME_PER_MOVE

class myTimer:
    def __init__(self):
        self.start_time = datetime.utcnow()

    def getRuntime(self):
        return (datetime.utcnow() - self.start_time).total_seconds()

    def getEndtime(self):
        return datetime.utcnow()

class spaceState(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

class Board:
    game_count = 0

    # Default initializer for the board Class
    def __init__(self):
        self.gameBoard = [[spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                          [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                          [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                          [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.BLACK,spaceState.WHITE,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                          [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.WHITE,spaceState.BLACK,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                          [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                          [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                          [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY]]
        self.state = 0
        self.turn = spaceState.BLACK
        self.moveTime = moveTimeout*1000
        self.moveIndex = 0

    # is the input move one of the legal moves?
    # This function is used to determine the number to display on the board
    def isLegalMove(self, inputBoard, pieceColor, row, column):
        legalMoveSelection = 0
        rowCounter         = 0
        columnCounter      = 0
        xchange            = 0
        ychange            = 0
        rowIterator        = 0
        moveCount          = 0
        NextBoardSpace     = 0

        for rowCounter in range(0,8):
            for columnCounter in range(0,8):
                if(inputBoard[rowCounter][columnCounter] == spaceState.EMPTY):
                    for xchange in range(-1, 2):
                        for ychange in range(-1, 2):
                            if (rowCounter + xchange >= 0 and rowCounter + xchange <=7 and columnCounter + ychange >= 0 and columnCounter + ychange <=7 ):
                                if(pieceColor == inputBoard[rowCounter+xchange][columnCounter+ychange] or \
                                   inputBoard[rowCounter+xchange][columnCounter+ychange] == spaceState.EMPTY):
                                    # do nothing since cant move do to this direction
                                    pass
                                else:
                                    for rowIterator in range (2,8):
                                        if NextBoardSpace != 0:
                                            break
                                        elif((rowCounter+rowIterator*xchange >= 0) and (rowCounter+rowIterator*xchange) <=7 and \
                                           (columnCounter+rowIterator*ychange >= 0) and (columnCounter+rowIterator*ychange <=7) ):
                                            
                                            # if a same piece is found in direction
                                            if(inputBoard[rowCounter+rowIterator*xchange][columnCounter+rowIterator*ychange] == pieceColor):
                                                moveCount = moveCount + 1
                                                if (rowCounter == row and columnCounter == column):
                                                    legalMoveSelection = moveCount

                                                # This move is determined to be legal and we can move on to the next boardSpace to see if it is legal
                                                NextBoardSpace = 1
                                            
                                            # if empty spot found in direction
                                            elif (inputBoard[rowCounter+rowIterator*xchange][columnCounter+rowIterator*ychange] == spaceState.EMPTY):
                                                break
                                        else:
                                            break
                            
                                    if NextBoardSpace != 0:
                                        break
                            
                            if NextBoardSpace != 0:
                                break
                        if NextBoardSpace != 0:
                            break
                NextBoardSpace = 0

        return legalMoveSelection

    # display the board using command shell coloring
    def display(self, inputBoard, pieceColor):
        moveNumber = 0
        currentRow = ""
        numStr1 = ""
        numStr2 = ""

        # top of the row with all empty spaces
        topRow =  "   \033[40;32;2;7m|    ||    |" + \
                  "\033[40;32;2;7m|    ||    |" + \
                  "\033[40;32;2;7m|    ||    |" + \
                  "\033[40;32;2;7m|    ||    |\033[0m"

        # Bottom of the row with all empty spaces
        bottomRow = "   \033[40;32;2;7m|____||____|" + \
                    "\033[40;32;2;7m|____||____|" + \
                    "\033[40;32;2;7m|____||____|" + \
                    "\033[40;32;2;7m|____||____|\033[0m"

        # Top row border
        topBorder = "   \033[40;32;2;7m____________" + \
                    "\033[40;32;2;7m____________" + \
                    "\033[40;32;2;7m____________" + \
                    "\033[40;32;2;7m____________\033[0m"

        # An individual spot display
        spot = "\033[40;32;2;7m "

        # Black Piece Spot display
        blackPiece = "\033[47;30;7m  "

        # White Piece Spot display
        whitePiece = "\033[40;37;7m  "

        # Black player move location display
        blackMoveOption = "\033[47;32;2;7m"

        # White player move location display
        whiteMoveOption = "\033[40;32;2;7m"

        # Empty board space display
        emptySpace = "\033[0m"

        # Normal Font
        normal = "\033[0m";

        # showing which player is what color
        print("Player 1 -> \033[47;30;7mBlack" + normal)
        print("Player 2 -> \033[40;37;7mWhite" + normal)

        # display top boarder with numbers
        print("     00    01    02    03    04    05    06    07")
        print(topBorder);

        # for each row diplay the relevant row
        for rowCounter in range (0,8):
            # print the top row
            print(topRow)

            # print the row counter on the left
            currentRow = str(rowCounter) + "  "

            # display each column in the row accordingly
            for columnCounter in range(0,8):
                # column empty space
                currentRow = currentRow + "\033[40;32;2;7m|" + spot + emptySpace
                
                # else if the game board shows this is a valid move for the current player's turn
                moveNumber = self.isLegalMove(inputBoard,pieceColor,rowCounter,columnCounter)
                
                # if the game board shows there is a black piece in the current row / column board space
                if (inputBoard[rowCounter][columnCounter] == spaceState.BLACK):
                    currentRow = currentRow + blackPiece

                # else if the game board shows there is a white piece in the current row / column board space
                elif (inputBoard[rowCounter][columnCounter] == spaceState.WHITE):
                    currentRow = currentRow + whitePiece

                elif (moveNumber != 0):
                    if (math.floor(moveNumber/10) != 0):
                        numStr1 = str(math.floor(moveNumber/10))
                    else:
                        numStr1 = " "
                    numStr2 = str(moveNumber % 10)

                    if (pieceColor == spaceState.WHITE):
                        currentRow = currentRow + blackMoveOption + numStr1 + numStr2
                    else:
                        currentRow = currentRow + whiteMoveOption + numStr1 + numStr2
                else:
                    currentRow = currentRow + spot + spot + emptySpace
                currentRow = currentRow + spot + "|" + normal
            print(currentRow)
            print(bottomRow)

    # set the game state
    def setState (self, inState):
        # state 0 is game is active
        # state 1 is game is over
        self.state = inState

    # initialize the game by requesting information from the user and starting the game
    def init (self):
        inputTime = moveTimeout
        print("How much time should the AI take on its turn (in seconds): " + str(inputTime/1000))
        self.moveTime = (int)(inputTime)
        print("")
        return 0

    # initializing the board if it is requested from the user
    def initBoard (self):
        #val = input("Do you want to input a non-default inital board state? (N/y): ")
        val = "N"
        if (val == ""):
            return self.gameBoard
        if (val[0] == 'y' or val[0] == 'Y'):
            filename = input("Input the name of the file containing the board state: ")
            self.gameBoard = getBoard(filename)
        return self.gameBoard
        
    # get an input board from the input filename
    def getBoard (self, filename):
        outBoard= [[spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                   [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                   [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                   [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.BLACK,spaceState.WHITE,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                   [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.WHITE,spaceState.BLACK,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                   [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                   [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                   [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY]]

        print("Opening and initializing based on file: " + filename)
        # ifstream inFile(filename)

        # while (getline(inFile, line))
        # {
        #         lineCount++;
        #         istringstream iss(line);
        #         if (lineCount > 0 && lineCount < 9)
        #         {
        #             columnLineCount = 0;
        #             pieceCount = 0;
        #             while (pieceCount < 9) {
        #                 if(line[columnLineCount] == '0' )
        #                 {
        #                     outBoard[lineCount-1][pieceCount] = spaceState.EMPTY;
        #                     pieceCount++;
        #                 }
        #                 else if ( line[columnLineCount] == '1') {
        #                     outBoard[lineCount-1][pieceCount] = spaceState.BLACK;
        #                     pieceCount++;
        #                 }
        #                 else if (line[columnLineCount] == '2') {
        #                     outBoard[lineCount-1][pieceCount] = spaceState.WHITE;
        #                     pieceCount++;
        #                 }
        #                 columnLineCount++;
        #             }
        #         }
        #         else if (lineCount == 9)
        #         {
        #             columnLineCount = 0;
        #             pieceCount = 0;
        #             while (pieceCount < 1)
        #             {
        #                 if(line[columnLineCount] == '1')
        #                 {
        #                     turn = spaceState.BLACK;
        #                     pieceCount++;
        #                 }
        #                 else if (line[columnLineCount] == '2')
        #                 {
        #                     turn = spaceState.WHITE;
        #                     pieceCount++;
        #                 }
        #                 columnLineCount++;
        #             }
        #         }
        #         else if (lineCount == 10)
        #         {
        #             //need to convert string to float
        #             AI_Time = atof(line.c_str());
        #             if( !AI_Time || AI_Time <= 0)
        #             {
        #                 cout << "NOT A VALID ENTRY, Selecting AI move time to: 2 Seconds" << endl;
        #             }
        #             else {
        #                 moveTime = (int)(1000*AI_Time);
        #                 cout << "Computer Time: " << AI_Time << " Seconds" << endl;
        #             }
        #         }
        # }
        # print("")
        return outBoard;
        
    # set the object's board to the input board
    def setBoard (self, inputBoard):
        for row in range(0,8):
            for column in range(0,8):
                self.gameBoard[row][column] = inputBoard[row][column]
    
    # input the current player and the current board
    # output the list of legal moves for the current player
    def legalMoves (self,inputBoard,pieceColor):
        rowCounter         = 0
        columnCounter      = 0
        xchange            = 0
        ychange            = 0
        rowIterator        = 0
        moveCount          = 0
        NextBoardSpace     = 0
        moves = [[]]
        oldBoard = copy(inputBoard)

        for rowCounter in range(0,8):
            for columnCounter in range(0,8):
                if(inputBoard[rowCounter][columnCounter] == spaceState.EMPTY):
                    for xchange in range(-1, 2):
                        for ychange in range(-1, 2):
                            if (rowCounter + xchange >= 0 and rowCounter + xchange <=7 and columnCounter + ychange >= 0 and columnCounter + ychange <=7 ):
                                if(pieceColor == inputBoard[rowCounter+xchange][columnCounter+ychange] or \
                                   inputBoard[rowCounter+xchange][columnCounter+ychange] == spaceState.EMPTY):
                                    # do nothing since cant move do to this direction
                                    pass
                                else:
                                    for rowIterator in range (2,8):
                                        if NextBoardSpace != 0:
                                            break
                                        elif((rowCounter+rowIterator*xchange >= 0) and (rowCounter+rowIterator*xchange) <=7 and \
                                           (columnCounter+rowIterator*ychange >= 0) and (columnCounter+rowIterator*ychange <=7) ):
                                            
                                            # if a same piece is found in direction
                                            if(inputBoard[rowCounter+rowIterator*xchange][columnCounter+rowIterator*ychange] == pieceColor):
                                                if moveCount != 0:
                                                    moves.append([])
                                                moves[moveCount] = self.pseudoplay(inputBoard,rowCounter,columnCounter,pieceColor)
                                                inputBoard = copy(oldBoard)
                                                moveCount = moveCount + 1
                                                
                                                # This move is determined to be legal and we can move on to the next boardSpace to see if it is legal
                                                NextBoardSpace = 1
                                            
                                            # if empty spot found in direction
                                            elif (inputBoard[rowCounter+rowIterator*xchange][columnCounter+rowIterator*ychange] == spaceState.EMPTY):
                                                break
                                        else:
                                            break
                                    if NextBoardSpace != 0:
                                        break
                            
                            if NextBoardSpace != 0:
                                break
                        if NextBoardSpace != 0:
                            break
                NextBoardSpace = 0
        return moves
    
    # return a count of moves given the array of available moves
    def moveCount (self, moves):
        if moves == [[]]:
            return 0
        count = len(moves)
        return count
    
    # rotate a piece from black to white or white to black
    def changePiece (self, pieceColor):
        if (pieceColor == spaceState.WHITE):
            return spaceState.BLACK
        else:
            return spaceState.WHITE
    
    # switch the current player's turn
    def switchTurn (self):
        if (self.turn == spaceState.BLACK):
            self.turn = spaceState.WHITE
        elif (self.turn == spaceState.WHITE):
            self.turn = spaceState.BLACK
        return 0
    
    # count the amount of white pieces and count the amount of black pieces
    # compare which one is larger and report that they won
    def winCheck (self, inputBoard):
        
        # initial counts
        whiteCount = 0
        blackCount = 0

        for row in range(0,8):
            for column in range(0,8):
                if (inputBoard[row][column] == spaceState.WHITE):
                    whiteCount = whiteCount + 1
                elif (inputBoard[row][column] == spaceState.BLACK):
                    blackCount = blackCount + 1

        if (blackCount > whiteCount):
            print("black wins: " + str(blackCount) + " - " + str(whiteCount))
            return 1
        elif (whiteCount > blackCount):
            print("white wins: " + str(whiteCount) + " - " + str(blackCount))
            return 2
        elif(whiteCount == blackCount):
            print("tie: " + str(whiteCount) + " - " + str(blackCount))
            return 3;
        else:
            return 0
    
    # return the number of empty spaces left on the board
    def movesLeft (self):
        numMovesLeft = 0
        for row in range(0,8):
            for column in range(0,8):
                if (self.gameBoard[row][column] == spaceState.EMPTY):
                    numMovesLeft = numMovesLeft + 1
        return numMovesLeft

    # This is the function that needs to be requested from the client to the server
    def moveSelect (self, moveMax):

        mtime             = 0
        seconds           = 0 
        useconds          = 0
        moveSelection     = 0
        tempmoveSelection = 0
        totalMovesLeft    = 0
        inputStr          = ""
        copyObject = Board()
        copyBoard  = copyObject.gameBoard
        for i in range (0,8):
            for j in range(0,8):
                copyBoard[i][j] = self.gameBoard[i][j]

        # temporary for testing
        # return random.randint(1,moveMax)
        depth = 1
        a = -1*POSINF
        b = POSINF
        hval = 0

        cplayer = self.turn
        totalMovesLeft = self.movesLeft()
        start_t = time.time()
        end_t = time.time()
        mtime = end_t-start_t

        while (1):
            #figure out what moveSelection we should chose
            if (moveMax == 1):
                moveSelection = 1
                break
            hval = self.alphabeta(copyBoard, depth, a, b, self.turn, cplayer, tempmoveSelection, start_t, end_t)
            if (hval == NOHEURVAL or depth > totalMovesLeft):
                break
            else:
                moveSelection = self.moveIndex + 1
                if (depth > 3 and depth < 8):
                    print("At depth: " + str(depth) + " move number: " + str(moveSelection) + " hval: " + str(hval))
                depth = depth + 1

        end_t = time.time()
        mtime = (end_t-start_t)*1000

        # print("At depth: " + str(depth-1) + ", Selecting Move: " + str(moveSelection))
        # print("Elapsed time: " + str(mtime) + " milliseconds")

        return moveSelection;
    
    # This is the alphabeta algorithm called by moveSelect
    # Move select will be ported to a separate piece of software which will be developed by the VM users
    def alphabeta (self, inputBoard, depth, a, b, pieceColor, playerTurn, moveIndex, startTime, endTime):
       # ind is the pointer to moveSelection only passed in when first called
        tempv = 0
        v = 0
        i = 0
        mtime = 0 
        seconds = 0 
        useconds = 0
        nextMoves = [[]]

        endTime = time.time()
        mtime = (endTime-startTime)*1000

        if (mtime + RETOVERHEAD > self.moveTime and v != POSINF and v != -1*POSINF):
            return NOHEURVAL

        nextMoves = self.AIMoves(inputBoard,playerTurn)
        if (depth == 0 or nextMoves == [[]]):
            if (pieceColor == spaceState.BLACK):
                v = self.heuristicFunction0(inputBoard,pieceColor)

            elif (pieceColor == spaceState.WHITE):
                v = self.heuristicFunction1(inputBoard,pieceColor)

        elif (playerTurn == pieceColor):
            v = -1*POSINF
            playerTurn = self.changePiece(playerTurn)
            if (nextMoves[i] != []):
                while (i < len(nextMoves)):
                    tempv = self.alphabeta(nextMoves[i], depth - 1, a, b, pieceColor, playerTurn, -1,startTime,endTime)
                    if (v < tempv):
                        v = tempv
                        if (moveIndex != -1):
                            self.moveIndex = i 
                            # print("At depth: " + str(depth) + " best move is: " + str(self.moveIndex + 1) + " with hval = " + str(v))
                    if b >= v:
                        b = v
                    if b <= a:
                        break
                    i = i + 1
        else:
            v = POSINF
            playerTurn = self.changePiece(playerTurn)
            if (nextMoves[i] != []):
                while (i < len(nextMoves)):
                    tempv = self.alphabeta(nextMoves[i], depth - 1, a, b, pieceColor, playerTurn, -1, startTime, endTime)
                    if (v >= tempv):
                        v = tempv
                    if b >= v:
                        b = v
                    if b <= a:
                        break
                    i = i + 1
        return v
    
    # pass in the current board and current player's turn
    # output the list of moves for the AI
    def AIMoves (self, inputBoard, pieceColor):
        rowCounter         = 0
        columnCounter      = 0
        xchange            = 0
        ychange            = 0
        rowIterator        = 0
        moveCount          = 0
        NextBoardSpace     = 0
        moves = [[]]
        oldBoard = copy(inputBoard)

        for rowCounter in range(0,8):
            for columnCounter in range(0,8):
                if(inputBoard[rowCounter][columnCounter] == spaceState.EMPTY):
                    for xchange in range(-1, 2):
                        for ychange in range(-1, 2):
                            if (rowCounter + xchange >= 0 and rowCounter + xchange <=7 and columnCounter + ychange >= 0 and columnCounter + ychange <=7 ):
                                if(pieceColor == inputBoard[rowCounter+xchange][columnCounter+ychange] or \
                                   inputBoard[rowCounter+xchange][columnCounter+ychange] == spaceState.EMPTY):
                                    # do nothing since cant move do to this direction
                                    pass
                                else:
                                    for rowIterator in range (2,8):
                                        if NextBoardSpace != 0:
                                            break
                                        elif((rowCounter+rowIterator*xchange >= 0) and (rowCounter+rowIterator*xchange) <=7 and \
                                           (columnCounter+rowIterator*ychange >= 0) and (columnCounter+rowIterator*ychange <=7) ):
                                            
                                            # if a same piece is found in direction
                                            if(inputBoard[rowCounter+rowIterator*xchange][columnCounter+rowIterator*ychange] == pieceColor):
                                                if moveCount != 0:
                                                    moves.append([])
                                                moves[moveCount] = self.pseudoplay(inputBoard,rowCounter,columnCounter,pieceColor);
                                                inputBoard = copy(oldBoard)
                                                moveCount = moveCount + 1

                                                # This move is determined to be legal and we can move on to the next boardSpace to see if it is legal
                                                NextBoardSpace = 1
                                            
                                            # if empty spot found in direction
                                            elif (inputBoard[rowCounter+rowIterator*xchange][columnCounter+rowIterator*ychange] == spaceState.EMPTY):
                                                break
                                        else:
                                            break
                            
                                    if NextBoardSpace != 0:
                                        break
                            
                            if NextBoardSpace != 0:
                                break
                        if NextBoardSpace != 0:
                            break
                NextBoardSpace = 0

        return moves

    # input the current board, current player's turn, and selected move on the board
    # output the resulting board IF we are playing in the selected spot
    def pseudoplay (self, inputBoard, rowSelect, columnSelect, pieceColor):
        xchange       = 0
        ychange       = 0
        rowCounter    = 0
        columnCounter = 0

        pseudoObject = Board()
        pseudoBoard = pseudoObject.gameBoard
        for i in range (0,8):
            for j in range(0,8):
                pseudoBoard[i][j] = inputBoard[i][j]

        for xchange in range(-1,2):
            for ychange in range(-1,2):
                # if tile is a valid board space
                if (rowSelect+xchange >= 0 and \
                    rowSelect+xchange <= 7 and \
                    columnSelect+ychange >= 0 and \
                    columnSelect+ychange <= 7 ):
                    
                    # if the next tile is empty or the same as the players piece
                    if(pieceColor == inputBoard[rowSelect+xchange][columnSelect+ychange] or \
                    inputBoard[rowSelect+xchange][columnSelect+ychange] == spaceState.EMPTY):
                        pass 
                    # the next tile is the opponents piece
                    else:
                        # search for a piece of the same type in a direction
                        for rowCounter in range(2,8):
                            # if tile is a valid board space
                            
                            if(rowSelect+rowCounter*xchange >= 0 and \
                               rowSelect+rowCounter*xchange <=7 and \
                               columnSelect+rowCounter*ychange >= 0 and \
                               columnSelect+rowCounter*ychange <=7 ):
                                
                                # if a same piece is found in direction
                                if(inputBoard[rowSelect+rowCounter*xchange][columnSelect+rowCounter*ychange] == pieceColor):
                                    for columnCounter in range(0,rowCounter):
                                        pseudoBoard[rowSelect+columnCounter*xchange][columnSelect+columnCounter*ychange] = pieceColor
                                    break
                                    
                                
                                # if empty spot found in direction
                                elif (inputBoard[rowSelect+rowCounter*xchange][columnSelect+rowCounter*ychange] == spaceState.EMPTY):
                                    break
                            
                            else:
                                break
        return pseudoBoard
    
    # input takes in the current player's turn and the current game board
    # output a zero sum value representative of the who is winning at that moment
    def heuristicFunction0 (self, inputBoard, pieceColor):
        #ensure the heurstic is zero sum!
        val = 0;
        corner = 0
        for i in range(0,8):
            for j in range(0,8):
                if (inputBoard[i][j] == pieceColor):
                    val = val - 1
                elif (inputBoard[i][j] != spaceState.EMPTY):
                    val = val + 1
        
        if inputBoard[0][0] == pieceColor:
            corner = corner - 1
        elif inputBoard[0][0] != spaceState.EMPTY:
            corner = corner + 1
        
        if inputBoard[7][0] == pieceColor:
            corner = corner - 1
        elif inputBoard[7][0] != spaceState.EMPTY:
            corner = corner + 1

        if inputBoard[0][7] == pieceColor:
            corner = corner - 1
        elif inputBoard[0][7] != spaceState.EMPTY:
            corner = corner + 1

        if inputBoard[7][7] == pieceColor:
            corner = corner - 1
        elif inputBoard[7][7] != spaceState.EMPTY:
            corner = corner + 1

        val = val*10 + corner*300 + random.randint(-4,4)
        return val

    # input takes in the current player's turn and the current game board
    # output a zero sum value representative of the who is winning at that moment
    def heuristicFunction1(self, inputBoard, pieceColor):
        #ensure the heurstic is zero sum!
        val = 0;
        corner = 0
        for i in range(0,8):
            for j in range(0,8):
                if (inputBoard[i][j] == pieceColor):
                    val = val + 1
                elif (inputBoard[i][j] != spaceState.EMPTY):
                    val = val - 1
        
        if inputBoard[0][0] == pieceColor:
            corner = corner + 1
        elif inputBoard[0][0] != spaceState.EMPTY:
            corner = corner - 1
        
        if inputBoard[7][0] == pieceColor:
            corner = corner + 1
        elif inputBoard[7][0] != spaceState.EMPTY:
            corner = corner - 1

        if inputBoard[0][7] == pieceColor:
            corner = corner + 1
        elif inputBoard[0][7] != spaceState.EMPTY:
            corner = corner - 1

        if inputBoard[7][7] == pieceColor:
            corner = corner + 1
        elif inputBoard[7][7] != spaceState.EMPTY:
            corner = corner - 1

        val = val*10 + corner*300 + random.randint(-4,4)
        return val