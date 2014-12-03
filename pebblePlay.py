'''
Created on Nov 16, 2014

@author: allisonholt
'''
#!/usr/bin/python
from __builtin__ import True
from macerrors import nilHandleErr
from findertools import move

#Heuristic Board: 2D-Array of Lists         -- hBoard[][]()
#Game Board: 2D-Array of Ints             -- gameBoard[][]

# Constants for referencing players
PLAYER1 = 0  #player A
PLAYER2 = 1  #player B

# Global "Hash Table"
transTable = {}

#global variables
depthForCutOffTest = 0

def heuristicFunction1(currentPlayer, gameBoardIn):
    totalPlayerPebs = 0
    for i in range(len(gameBoardIn[currentPlayer])):
        totalPlayerPebs += gameBoardIn[currentPlayer][i]
    return totalPlayerPebs

#Adam's function
def utilityH2(currentPlayer, gameBoard):
    playerPebbles = 0
    opponentPebbles = 0

    for i in range( len( gameBoard[currentPlayer] ) ):
        playerPebbles += gameBoard[currentPlayer][i]
        opponentPebbles += gameBoard[not(currentPlayer)][i]

    return playerPebbles - opponentPebbles

#########################################
#                                        #
#     Transposition Table Functionality   #
#                                        #
#########################################

def boardToHashIndex(gameBoard, currentPlayer):
    hashIndex1 = ""
    hashIndex2 = ""

    for i in range( len( gameBoard[PLAYER1] ) ):
        hashIndex1 += str(gameBoard[PLAYER1][i])
        hashIndex2 += str(gameBoard[PLAYER2][i])

    return hashIndex1 + hashIndex2

def getMinimaxFromHashTable(gameBoard):
    hashIndex = boardToHashIndex(gameBoard)

    if( hashIndex in transTable ):
        returnValue = transTable[hashIndex]
    else:
        returnValue = False

    return returnValue

def storeMinimaxInHashTable(gameBoard, minimaxValue):
    global transTable

    if( getMinimaxFromHashTable(gameBoard) == False ):
        hashIndex = boardToHashIndex(gameBoard)
        transTable[hashIndex] = minimaxValue
        return True
    else:
        return False

def result(state, action, currentPlayer):
    numberOfColumns = len(state[0])
    tempState = [[state[x][y] for y in range(numberOfColumns)] for x in range(2)]
    makeMove(tempState, currentPlayer, action)
    return tempState

def cutOffTest(state, depth):
    if (depth == depthForCutOffTest):
        return True
    elif (goalTest(state)):
        return True
    else:
        return False

def maxValue(state, alpha, beta, depth, pathStates, currentPlayer, heurValue, playerToMakeMove):
    if (state in pathStates):
        return float('-inf')
    if (cutOffTest(state, depth) == True):
        #check which utility is used
        if(heurValue == 1):
            return heuristicFunction1(currentPlayer, state)
        else:
            return utilityH2(currentPlayer, state)
    pathStates.append(state)
    v = float('-inf')
    for move in range(len(state[0])):
        if(state[playerToMakeMove][move] > 0):
            statePrime = result(state, move, playerToMakeMove)
            if (getMinimaxFromHashTable(state) != False): #statePrime in transTable
                vPrime = getMinimaxFromHashTable(state)
                #return
            else:
                vPrime = minValue(statePrime, alpha, beta, (depth + 1), pathStates, currentPlayer, heurValue, not(playerToMakeMove))
                storeMinimaxInHashTable(state, vPrime)
            if (vPrime > v):
                v = vPrime
            if (v >= beta):
                return v
            elif (v > alpha):
                alpha = v
    return v
            
    
def minValue(state, alpha, beta, depth, pathStates, currentPlayer, heurValue, playerToMakeMove):
    if (state in pathStates):
        return float('inf')
    if (cutOffTest(state, depth) == True):
        #check which utility is used
        if(heurValue == 1):
            return heuristicFunction1(currentPlayer, state)
        else:
            return utilityH2(currentPlayer, state)
    pathStates.append(state)
    v = float('inf')
    for move in range(len(state[0])):
        if(state[playerToMakeMove][move] > 0):
            statePrime = result(state, move, playerToMakeMove)
            if (getMinimaxFromHashTable(state) != False): #statePrime in transTable
                vPrime = getMinimaxFromHashTable(state)
                #return 
            else:
                vPrime = maxValue(statePrime, alpha, beta, (depth + 1), pathStates, currentPlayer, heurValue, not(playerToMakeMove))
                storeMinimaxInHashTable(state, vPrime)
            if (vPrime < v):
                v = vPrime
            if (v <= alpha):
                return v
            elif (v > beta):
                beta = v
    return v
    
def alphaBetaSearch(state, depth, currentPlayer, heurValue): #state is game board and depth is the ply
    playerToMakeMove = currentPlayer
    v = float('-inf')
    a = None
    alpha = float('-inf')
    beta = float('inf')
    pathStates = []
    for move in range(len(state[0])): #each column is a move
        #if state is goal state
        if(state[currentPlayer][move] > 0):
            statePrime = result(state, move, currentPlayer)  #need to make fake gameboard?
            vPrime = maxValue(statePrime, alpha, beta, depth, pathStates, currentPlayer, heurValue, playerToMakeMove) #had as min in algorithm, but shouldn't it be max?
            if (vPrime > v):
                v = vPrime
                a = move
            if (v >= beta):
                return a
            elif (v > alpha):
                alpha = v
    return a

def makeMove(gameBoardIn, currentPlayersMove, colToMoveFromIn):
    if (currentPlayersMove == PLAYER1):
        pebsToMove = gameBoardIn[currentPlayersMove][colToMoveFromIn]
        gameBoardIn[currentPlayersMove][colToMoveFromIn] = 0
        maxColIndex = len(gameBoardIn[currentPlayersMove]) - 1
        if(colToMoveFromIn == maxColIndex):
            currentRow = PLAYER2
            currentColumn = maxColIndex
        else:
            currentRow = currentPlayersMove
            currentColumn = (colToMoveFromIn + 1)
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
    else: #player 2
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
    rowString = "Player 1:             "
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
    depthForCutOffTest = ply
    print ""
    
    notProperInput = True
    while(notProperInput):
        runOrStep = int(input("How are you viewing the game?  0-run through or 1-step through:  "))
        if ((runOrStep == 0) or (runOrStep == 1)):
            notProperInput = False
    print "" 
      
    if(runOrStep == 1):
        notProperInput = True
        while(notProperInput):
            userPlaying = int(input("Is the computer playing itself (enter 0) or are you playing against the computer (enter 1)?:  "))
            if ((userPlaying == 0) or (userPlaying == 1)):
                notProperInput = False
                
    if(runOrStep == 0):  #means comp must be playing itself
        userPlaying = 0
    print ""
    
    if(userPlaying):
        notProperInput = True
        print "Heuristics"
        print "1) Number of Pebbles of Player"
        print "2) Difference Between Your Pebbles and Opponent's Pebbles"
        while(notProperInput):
            hValue = int(input("Which heuristic do you want computer to use?  1 or 2:  "))
            if((hValue == 1) or (hValue == 2)):
                notProperInput = False
        print""
            
        notProperInput = True
        print "Planning Algorithms"
        print "1) And-Or Search"
        print "2) Alpha-Beta Minimax"
        while(notProperInput):
            algValue = int(input("Which algorithm do you want computer to use?  1 or 2:  "))
            if((algValue == 1) or (algValue == 2)):
                notProperInput = False
        print ""
        
    else:
        notProperInput = True
        print "Heuristics"
        print "1) Number of Pebbles of Player"
        print "2) Difference Between Your Pebbles and Opponent's Pebbles"
        while(notProperInput):
            hValuePlayer1 = int(input("Which heuristic do you want to use for player 1?  1 or 2:  "))
            if((hValuePlayer1 == 1) or (hValuePlayer1 == 2)):
                notProperInput = False
        print ""        
        
        notProperInput = True
        print "Heuristics"
        print "1) Number of Pebbles of Player"
        print "2) Difference Between Your Pebbles and Opponent's Pebbles"
        while(notProperInput):
            hValuePlayer2 = int(input("Which heuristic do you want to use for player 2?  1 or 2:  "))
            if((hValuePlayer2 == 1) or (hValuePlayer2 == 2)):
                notProperInput = False
        print ""
                
        notProperInput = True
        print "Planning Algorithms"
        print "1) And-Or Search"
        print "2) Alpha-Beta Minimax"
        while(notProperInput):
            algValuePlayer1 = int(input("Which algorithm do you want to use for player 1?  1 or 2:  "))
            if((algValuePlayer1 == 1) or (algValuePlayer1 == 2)):
                notProperInput = False
        print ""
        
        notProperInput = True
        print "Planning Algorithms"
        print "1) And-Or Search"
        print "2) Alpha-Beta Minimax"
        while(notProperInput):
            algValuePlayer2 = int(input("Which algorithm do you want to use for player 2?  1 or 2:  "))
            if((algValuePlayer2 == 1) or (algValuePlayer2 == 2)):
                notProperInput = False
        print ""

    '''
    Set Up Game Board
    '''
    gameBoard = [[pebsPerSq for y in range(numCols)] for x in range(2)]  #range vs xrange?
    
    #if (runOrStep == 0): #when running through
        #print "TBD"
    #else:  #means stepping through
    currentMove = PLAYER1
    if(userPlaying):
        print "You are Player 2"
        while(not(goalTest(gameBoard))):
            '''
            Use Function to Print Game Board
            '''
            printGameBoard(gameBoard)
        
            if(currentMove == PLAYER1):
                print ""
                print "Player 1's move"
                print ""
                    
                if(algValue == 1):
                    print "not implemented yet"
                else:
                    colToMoveFrom = alphaBetaSearch(gameBoard, 0, PLAYER1, hValue)
                    makeMove(gameBoard, PLAYER1, colToMoveFrom)
                    debugString = "Algorithm returned:  "
                    debugString += str(colToMoveFrom)
                    print debugString
                    print ""
            
                currentMove = PLAYER2
                
            else:
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
        #step through with two computers or run with two computers
        printGameBoard(gameBoard)
        while(not(goalTest(gameBoard))):
            '''
            Use Function to Print Game Board
            '''
            #printGameBoard(gameBoard)
            
            '''
            if(runOrStep == 1):
                notProperInput = True
                while(notProperInput):
                    runOrStep = int(input("Would you like to run though the rest of the game or continue stepping through?  0-run through or 1-step through:  "))
                    if ((runOrStep == 0) or (runOrStep == 1)):
                        notProperInput = False
            '''
            
            if(currentMove == PLAYER1):
                print ""
                print "Player 1's move"
                print ""
                    
                if(algValuePlayer1 == 1):
                    print "not implemented yet"
                else:
                    colToMoveFrom = alphaBetaSearch(gameBoard, 0, PLAYER1, hValuePlayer1)
                    makeMove(gameBoard, PLAYER1, colToMoveFrom)
                    debugString = "Algorithm returned:  "
                    debugString += str(colToMoveFrom)
                    print debugString
                    print ""
            
                currentMove = PLAYER2
                
                printGameBoard(gameBoard)
                
                if(runOrStep == 1 and not(goalTest(gameBoard))):
                    notProperInput = True
                    while(notProperInput):
                        runOrStep = int(input("Would you like to run though the rest of the game or continue stepping through?  0-run through or 1-step through:  "))
                        if ((runOrStep == 0) or (runOrStep == 1)):
                            notProperInput = False
                        
            else:
                print ""
                print "Player 2's move"
                print ""
                    
                if(algValuePlayer2 == 1):
                    print "not implemented yet"
                else:
                    colToMoveFrom = alphaBetaSearch(gameBoard, 0, PLAYER2, hValuePlayer2)
                    makeMove(gameBoard, PLAYER2, colToMoveFrom)
                    debugString = "Algorithm returned:  "
                    debugString += str(colToMoveFrom)
                    print debugString
                    print ""
            
                currentMove = PLAYER1
                
                printGameBoard(gameBoard)
                
                if(runOrStep == 1 and not(goalTest(gameBoard))):
                    notProperInput = True
                    while(notProperInput):
                        runOrStep = int(input("Would you like to run though the rest of the game or continue stepping through?  0-run through or 1-step through:  "))
                        if ((runOrStep == 0) or (runOrStep == 1)):
                            notProperInput = False
        print ""
        print "Final Game Board:"
            
        printGameBoard(gameBoard)
            
        print ""
        if(heuristicFunction1(PLAYER2, gameBoard) != 0):
            print "Player 2 won!"
        else:
            print "Player 1 won!"
    
    return

if __name__ == '__main__':
    main()
    