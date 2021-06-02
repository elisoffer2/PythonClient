from enum import Enum
from OthelloClass import spaceState
from OthelloClass import Board

import sys

from enum import Enum

def main(argv):
    gameObject = Board()

    totalMoveCount = 0
    noMoveCount = 0
    moveSelection = 0

    gameObject.init()

    objectBoard = gameObject.initBoard()

    gameObject.setBoard(objectBoard)

    gameObject.display(gameObject.gameBoard, gameObject.turn)

    while (gameObject.state != 1):
        availableMoves = gameObject.legalMoves(gameObject.gameBoard,gameObject.turn)
        totalMoveCount = gameObject.moveCount(availableMoves)

        if (totalMoveCount != 0):
            # this function should be cut to request from the client VM
            moveSelection = gameObject.moveSelect(totalMoveCount)
            moveSelection = 2
            availableMoves = [[[spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.BLACK,spaceState.WHITE,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.WHITE,spaceState.BLACK,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY]], \
                              [[spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.BLACK,spaceState.WHITE,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.WHITE,spaceState.BLACK,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY], \
                              [spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY,spaceState.EMPTY]]]

            # the new board is the old board with the selected move applied
            # updated the board, set the object value and display it
            objectBoard = availableMoves[moveSelection-1]
            gameObject.setBoard(objectBoard)
            gameObject.display(gameObject.gameBoard,gameObject.changePiece(gameObject.turn))

            # reset the no move count
            noMoveCount = noMoveCount + 1
            # noMoveCount = 0
            print("")
        
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