from enum import Enum
import math
DEFAULT_TIME_PER_MOVE = 1

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
        self.moveTime = DEFAULT_TIME_PER_MOVE

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
        state = inState

    # initialize the game by requesting information from the user and starting the game
    def init (self):
        inputTime = DEFAULT_TIME_PER_MOVE
        print("How much time should the AI take on its turn (in seconds): " + str(inputTime))
        self.moveTime = (int)(1000*inputTime)
        print("")
        return 0

    # initializing the board if it is requested from the user
    def initBoard (self):
        val = input("Do you want to input a non-default inital board state? (N/y): ")
        if (val[0] == 'y' or val[0] == 'Y')
        {
            filename = input("Input the name of the file containing the board state: ");
            self.gameBoard = getBoard(filename);
        }
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
    
    # return a count of moves given the array of available moves
    def moveCount (self, moves):
        x = 1
    
    # rotate a piece from black to white or white to black
    def changePiece (self, pieceColor):
        x = 1
    
    # switch the current player's turn
    def switchTurn (self):
        x = 1
    
    # count the amount of white pieces and count the amount of black pieces
    # compare which one is larger and report that they won
    def winCheck (self, inputBoard):
        x = 1
    
    # return the number of empty spaces left on the board
    def movesLeft (self):
        x = 1
    
    # This is the function that needs to be requested from the client to the server
    def moveSelect (self, moveMax):
        return 2
    
    # This is the alphabeta algorithm called by moveSelect
    # Move select will be ported to a separate piece of software which will be developed by the VM users
    def alphabeta (self, inputBoard, depth, a, b, pieceColor, playerTurn, indicator, startTime, endTime):
        x = 1
    
    # pass in the current board and current player's turn
    # output the list of moves for the AI
    def AIMoves (self, inputboard, pieceColor):
        x = 1

    # input the current board, current player's turn, and selected move on the board
    # output the resulting board IF we are playing in the selected spot
    def pseudoplay (self, inputBoard, rowSelect, columnSelect, pieceColor):
        x = 1
    
    # input takes in the current player's turn and the current game board
    # output a zero sum value representative of the who is winning at that moment
    def heuristicFunction0 (self, inputBoard, pieceColor):
        x = 1

    # input takes in the current player's turn and the current game board
    # output a zero sum value representative of the who is winning at that moment
    def heuristicFunction1(self, inputBoard, pieceColor):
        x = 1