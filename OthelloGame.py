from enum import Enum
from OthelloClass import spaceState
from OthelloClass import Board
import time

import sys

from enum import Enum

def main(argv):
    gameObject = Board()

    gameType = 3
    totalMoveCount = 0
    noMoveCount = 0
    moveSelection = 0

    gameType = gameObject.init()

    objectBoard = gameObject.initBoard()

    gameObject.setBoard(objectBoard)

    gameObject.display(gameObject.gameBoard,gameObject.turn)

    while (gameObject.state != 1):
        inputBoard = gameObject.gameBoard
        inputTurn = gameObject.turn
        availableMoves = gameObject.legalMoves(inputBoard,inputTurn)

        totalMoveCount = gameObject.moveCount(availableMoves)
        #gameObject.display(gameObject.gameBoard,gameObject.changePiece(gameObject.turn))

        if (totalMoveCount != 0):
            # this function should be cut to request from the client VM
            moveSelection = gameObject.moveSelect(gameType, totalMoveCount)
            print("Selected Move: " + str(moveSelection))
            print("")

            # the new board is the old board with the selected move applied
            # updated the board, set the object value and display it
            objectBoard = availableMoves[moveSelection-1]
            gameObject.setBoard(objectBoard)
            gameObject.display(gameObject.gameBoard,gameObject.changePiece(gameObject.turn))

            # reset the no move count
            noMoveCount = 0
        
        else:
            noMoveCount = noMoveCount + 1
            if (noMoveCount >= 2):
                # Set State to game over since no one can play
                gameObject.setState(1)
            elif (noMoveCount == 1):
                # Skip the current player's turn as there are no moves to play
                print("Player " + str(gameObject.turn) + " has no moves.");
                print ("Skipping Turn: it is now Player " + str(gameObject.changePiece(gameObject.turn)) + "'s turn")
                gameObject.display(gameObject.gameBoard,gameObject.changePiece(gameObject.turn))
            
        # the current player has played and we switch the player's current turn
        gameObject.switchTurn()
        
    
    gameObject.winCheck(gameObject.gameBoard)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])