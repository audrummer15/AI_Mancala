'''
Created on Nov 16, 2014

@author: allisonholt
'''
#!/usr/bin/python
from __builtin__ import True

#Heuristic Board: 2D-Array of Lists         -- hBoard[][]()
#Game Board: 2D-Array of Ints             -- gameBoard[][]

# Constants for referencing players
PLAYER1 = 0
PLAYER2 = 1

def heuristicFunction1(currentPlayer, gameBoardIn):
    totalPlayerPebs = 0
    for i in range(len(gameBoardIn[currentPlayer])):
        totalPlayerPebs += gameBoardIn[currentPlayer][i]
    return totalPlayerPebs


def makeMove(gameBoardIn, currentPlayersMove, colToMoveFromIn):
    if (currentPlayersMove == PLAYER1):
        pebsToMove = gameBoardIn[currentPlayersMove][colToMoveFromIn]
        gameBoardIn[currentPlayersMove][colToMoveFromIn] = 0
        maxColIndex = len(gameBoardIn[currentPlayersMove]) - 1
        if(colToMoveFromIn == 0):
            currentRow = PLAYER2
            currentColumn = 0
        else:
            currentRow = currentPlayersMove
            currentColumn = (colToMoveFromIn - 1)
        while (pebsToMove > 0):
            gameBoardIn[currentRow][currentColumn] += 1
            pebsToMove -= 1
            if((currentColumn == 0) and (currentRow == PLAYER2)):
                currentRow = PLAYER1
            elif((currentColumn == maxColIndex) and (currentRow == PLAYER1)):
                currentRow = PLAYER2
            elif (currentRow == PLAYER2):
                currentColumn -= 1
            elif (currentRow == PLAYER1):
                currentColumn += 1
    else:
        pebsToMove = gameBoardIn[currentPlayersMove][colToMoveFromIn]
        gameBoardIn[currentPlayersMove][colToMoveFromIn] = 0
        maxColIndex = len(gameBoardIn[currentPlayersMove]) - 1
        if(colToMoveFromIn == 0):
            currentRow = PLAYER1
            currentColumn = 0
        else:
            currentRow = currentPlayersMove
            currentColumn = (colToMoveFromIn - 1)
        while (pebsToMove > 0):
            gameBoardIn[currentRow][currentColumn] += 1
            pebsToMove -= 1
            if((currentColumn == 0) and (currentRow == PLAYER2)):
                currentRow = PLAYER1
            elif((currentColumn == maxColIndex) and (currentRow == PLAYER1)):
                currentRow = PLAYER2
            elif (currentRow == PLAYER2):
                currentColumn -= 1
            elif (currentRow == PLAYER1):
                currentColumn += 1
    return
        

def goalTest(gameBoard):
    bPlayer1Empty = True
    bPlayer2Empty = True
    bGoalState = False

    for i in range( len( gameBoard[PLAYER1] ) ):
        if( gameBoard[PLAYER1][i] != 0 ):
            bPlayer1Empty = False

        if( gameBoard[PLAYER2][i] != 0 ):
            bPlayer2Empty = False

    if( bPlayer1Empty or bPlayer2Empty ):
        bGoalState = True

    return bGoalState

def printGameBoard(gameBoardIn):
    rowString = "Player 1 (Computer):  "
    for i in range(len(gameBoardIn[0])):
        rowString += "["
        rowString += str(gameBoardIn[0][i])
        rowString += "]"
    print rowString
    
    rowString = "Player 2:             "
    for i in range(len(gameBoardIn[1])):
        rowString += "["
        rowString += str(gameBoardIn[1][i])
        rowString += "]"
    print rowString
    return

def main():
    
    '''
    Collect User Input at Beginning of Program Execution
    '''
    numCols = int(input("Please enter the number of columns per player:  "))
    #print numCols #how does this make since...
    if (numCols < 2):
        print "There must be at least two columns"
        print "Updated the number of columns to 2"
        numCols = 2
    elif (numCols > 10):
        print "The max number of columns is 10"
        print "Updated the number of columns to 10"
        numCols = 10
    
    pebsPerSq = int(input("Please enter the number of pebbles per square:  "))
    ply = int(input("Please enter the number of plys:  "))
    
    notProperInput = True
    while(notProperInput):
        runOrStep = int(input("How are you viewing the game?  0-run through or 1-step through:  "))
        if ((runOrStep == 0) or (runOrStep == 1)):
            notProperInput = False
        
    if(runOrStep == 1):
        notProperInput = True
        while(notProperInput):
            userOrComp = int(input("Are you playing the game (enter 0) or watching the computer play itself(enter 1):  "))
            if ((userOrComp == 0) or (userOrComp == 1)):
                notProperInput = False

    notProperInput = True
    print "Heuristics"
    print "1) Number of Pebbles of Player"
    print "2) "
    while(notProperInput):
        hValue = int(input("Which heuristic do you want to use?  1 or 2:"))
        if((hValue == 1) or (hValue == 2)):
            notProperInput = False
            
    notProperInput = True
    print "Planning Algorithms"
    print "1) And-Or Search"
    print "2) Alpha-Beta Minimax"
    while(notProperInput):
        algValue = int(input("Which algorithm do you want to use?  1 or 2:"))
        if((algValue == 1) or (algValue == 2)):
            notProperInput = False
    print ""

    '''
    Set Up Game Board
    '''
    gameBoard = [[pebsPerSq for y in range(numCols)] for x in range(2)]  #range vs xrange?
    
    if (runOrStep == 0):
        print "TBD"
    else:  
        currentMove = PLAYER1
        if (userOrComp == 0):
            while(not(goalTest(gameBoard))):
                '''
                Use Function to Print Game Board
                '''
                printGameBoard(gameBoard)
        
                if(currentMove == PLAYER1):
                    print ""
                    print "Player 1's move"
                    print ""
            
                    currentMove = PLAYER2
                else:
                    '''
                    Calculates Player 2's Heuristic Value
                    '''
                    print ""
                    player2String = "Assuming you are player 2, your heuristic value is "
                    player2String += str(heuristicFunction1(PLAYER2, gameBoard))
                    print player2String
                    print ""
        
                    notValidInput = True
                    while (notValidInput):
                        colToMoveFrom = int(input("Which of your squares do you empty?  The numbering starts from the left with value 0:  "))
                        if((colToMoveFrom < 0) or (colToMoveFrom >= numCols)):
                            print "The column number is invalid.  Remember the numbering starts at 0."
                        elif(gameBoard[PLAYER2][colToMoveFrom] == 0):
                            print "This is an invalid move since you have no pebbles there."
                        else:
                            notValidInput = False
                
                    makeMove(gameBoard, PLAYER2, colToMoveFrom)
            
                    currentMove = PLAYER1
            print ""
            print "Final Game Board:"
            
            printGameBoard(gameBoard)
            
            print ""
            if(heuristicFunction1(PLAYER2, gameBoard) != 0):
                print "Congratulations you won!"
            else:
                print "Sorry you lost. Better luck next time."
        
        else:
            #step through with two computers
            temp = 0
    
    return

if __name__ == '__main__':
    main()
    