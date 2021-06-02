from enum import Enum

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
    
    return [legalMoveSelection]

        
    # display the board using command shell coloring
    def display(self, inputBoard, pieceColor):
        x = 1

    # set the game state
    def setState (self, inState):
        x = 1

    # initialize the game by requesting information from the user and starting the game
    def init (self):
        x = 1

    # initializing the board if it is requested from the user
    def initBoard (self):
        x = 1
        
    # get an input board from the input filename
    def getBoard (self, filename):
        x = 1
        
    # set the object's board to the input board
    def setBoard (self, inputBoard):
        x = 1
    
    # input the current player and the current board
    # output the list of legal moves for the current player
    def legalMoves (self,inputBoard,pieceColor):
        x = 1
    
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