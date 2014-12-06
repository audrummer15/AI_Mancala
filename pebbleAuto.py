'''
Created on Nov 16, 2014

@author: allisonholt
'''
#!/usr/bin/python
from __builtin__ import True
from macerrors import nilHandleErr
from findertools import move
from copy import deepcopy

import sys

#Heuristic Board: 2D-Array of Lists         -- hBoard[][]()
#Game Board: 2D-Array of Ints             -- gameBoard[][]

# Constants for referencing players
PLAYER1 = 0  #player A
PLAYER2 = 1  #player B

PLAYER = 0   #For redundancy
OPPONENT = 1 #For redundancy

# For referencing pieces of and-or return tuples
ACTION = 0
VALUE = 1

# Global "Hash Table"
transTable = {}

#global variables
depthForCutOffTest = 0

def main():

    if len(sys.argv) < 8:
        sys.exit()

    numCols = int( sys.argv[1])
    pebsPerSq = int(sys.argv[2])
    ply = int(sys.argv[3])
    depthForCutOffTest = ply
    runOrStep = 0
    userPlaying = 0
    hValuePlayer1 = int(sys.argv[4])
    hValuePlayer2 = int(sys.argv[5])
    algValuePlayer1 = int(sys.argv[6])
    algValuePlayer2 = int(sys.argv[7])

    '''Reset the results file so that no winner has been declared
        if game does not finish'''
    returnValue = 0
        
    f = open('auto_out.res', 'w')
    f.write(str(returnValue))
    f.close()

    '''
    Set Up Game Board
    '''
    gameBoard = [[pebsPerSq for y in range(numCols)] for x in range(2)]  #range vs xrange?

    #if (runOrStep == 0): #when running through
        #print "TBD"
    #else:  #means stepping through
    currentMove = PLAYER1
    if(userPlaying):
        print "Note:  You are Player 2"
        print ""
        while(not(goalTest(gameBoard))):
            '''
            Use Function to Print Game Board
            '''
            printGameBoard(gameBoard)
            print ""
        
            if(currentMove == PLAYER1):
                raw_input("Press enter to continue and see Player 1's next move.  ")
                
                print ""
                print "Player 1's move"
                print ""
                    
                if(algValue == 1):
                    colToMoveFrom = andOrGraphSearch(gameBoard, depthForCutOffTest, hValue, PLAYER1)
                    makeMove(gameBoard, PLAYER1, colToMoveFrom)
                    print "Algorithm returned: ", colToMoveFrom, "\n"
                else:
                    colToMoveFrom = alphaBetaSearch(gameBoard, 0, PLAYER1, hValue)
                    makeMove(gameBoard, PLAYER1, colToMoveFrom)
                    #debugString = "Algorithm returned:  "
                    #debugString += str(colToMoveFrom)
                    #print debugString
                    print ""
            
                currentMove = PLAYER2
                
            else:
                
                print ""
                print "Your move"
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
                print ""
                
                currentMove = PLAYER1
        print ""
        print "--END OF GAME RESULTS--"
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
            
            if(currentMove == PLAYER1):
                print ""
                print "Player 1's move"
                print ""
                    
                if(algValuePlayer1 == 1):
                    colToMoveFrom = andOrGraphSearch(gameBoard, depthForCutOffTest, hValuePlayer1, PLAYER1)
                    makeMove(gameBoard, PLAYER1, colToMoveFrom)
                    print "Algorithm returned: ", colToMoveFrom, "\n"
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
                    colToMoveFrom = andOrGraphSearch(gameBoard, depthForCutOffTest, hValuePlayer2, PLAYER2)
                    makeMove(gameBoard, PLAYER2, colToMoveFrom)
                    print "Algorithm returned: ", colToMoveFrom, "\n"
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
            returnValue = 2
        else:
            print "Player 1 won!"
            returnValue = 1

    f = open('auto_out.res', 'w')
    f.write(str(returnValue))
    f.close()

    return returnValue

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

def boardToHashIndex(gameBoard):
    if( not isValidBoard(gameBoard) ):
        return False

    hashIndex1 = ""
    hashIndex2 = ""

    for i in range( len( gameBoard[PLAYER] ) ):
        hashIndex1 += str(gameBoard[PLAYER][i])
        hashIndex2 += str(gameBoard[OPPONENT][i])

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

#########################################
#                                       #
# AND-OR Search Algorithm Functionality #
#                                       #
#########################################

def andOrGraphSearch(gameBoard, ply, heurValue, player):
    if( not isValidBoard(gameBoard) ):
        return False

    # Problem is the board given
    # State is the current state of the board
    return orSearch(gameBoard, [], ply, heurValue, player)[ACTION]


def orSearch(board, path, moves, heurValue, player):
    plan = False

    # If the board is a goal
    # or 
    # If we have hit our depth limit, 
    #   return the heuristic value of the current board
    #   The action parameter of the tuple doesn't matter, so return -infinity
    if goalTest(board) or moves <= 0: 
        if(heurValue == 1):
            return [float('-inf'), heuristicFunction1(player, board)]
        else:
            return [float('-inf'), utilityH2(player, board)]

    value = float('-inf')
    
    if boardToHashIndex(board) in path:
        return False

    for action in range( len( board[player] ) ):
        if board[player][action] != 0: #if the move is valid
            if moves > 1:
                newPath = deepcopy(path)
                newPath.insert(0, boardToHashIndex(board))
                newValue = andSearch( results(board, action, player), newPath, moves - 1, heurValue, player)
            else:
                if(heurValue == 1):
                    newValue = heuristicFunction1(player, result(board, action, player))
                else:
                    newValue = utilityH2(player, result(board, action, player))

            if newValue != False:
                if newValue > value:
                    value = newValue
                    plan = [action, newValue]

            if plan == False:
                plan = [action, value]

    return plan

def andSearch(states, path, moves, heurValue, player):
    if not states:
        return float('-inf')

    returnValue = 0

    for state in states:
        if moves <= 0:
            if(heurValue == 1):
                returnValue = returnValue + heuristicFunction1(player, state)
            else:
                returnValue = returnValue + utilityH2(player, state)
        else:
            newPlan = orSearch( state, path, moves - 1, heurValue, PLAYER )
            
            if newPlan == False:
                return False

            returnValue = returnValue + newPlan[VALUE]

    #return average of board heuristics
    if( len(states) != 0):
        return (returnValue / len(states))
    else:
        return returnValue


#results returns a list of states that are potentially presented after player makes a move
# and the opponent responds
def results(state, action, player):
    resultStates = []
    numberOfColumns = len(state[0])
    newState = [[state[x][y] for y in range(numberOfColumns)] for x in range(2)]

    newState = result(newState, action, player)

    if goalTest(newState):
        print "AO-RESULTS RETURN EMPTY"
        return resultStates

    opponent = 1 - player

    for action in range( numberOfColumns ):
        tempState = deepcopy(newState)
        if tempState[opponent][action] != 0:
            makeMove(tempState, opponent, action)
            resultStates.append(tempState)

    return resultStates

#########################################
#                                       #
#         Helper Functionality          #
#                                       #
#########################################

def isValidBoard(gameBoard):
    if( len(gameBoard) != 2 ):
        return False
    else:
        return True

if __name__ == '__main__':
    main()
    